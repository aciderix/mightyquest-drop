#!/usr/bin/env python3
"""
emu.py — Unicorn micro-emulation harness for the Mighty Quest PE32 client.

Unicorn is a CPU emulator only: no OS, no DLLs, no GPU. You CANNOT run the game
with it. What it is good for here is executing a *single isolated routine* —
feed registers/memory, run, read the result — to confirm a hypothesis without a
Windows box. Good targets: serializers (wire format), hashes/checksums, token
or signature derivation, small decoders. Bad targets: anything with a deep call
graph into the OS / curl / heap.

This harness:
  - maps every PE section at its real VA (zero-filling virtual padding),
  - sets up a stack and a sentinel return address,
  - stubs any CALL that leaves `.text` (broken IAT / imports) by returning a
    chosen value, so leaf-ish functions run to completion,
  - lazily maps zero pages on stray reads/writes to stay forgiving.

Example:
    from emu import Emu
    e = Emu("MightyQuest_unpacked_fixed (1).exe")
    # call a cdecl function at VA 0x00abc123 with two int args, read EAX:
    ret = e.call(0x00abc123, [0x10, 0x20])
    print(hex(ret))
    print(e.read(0x00bd0000, 64).hex())   # inspect output buffer

Run `python3 re/tools/emu.py --self-test` for a sanity check.
"""
from __future__ import annotations
import argparse, struct, sys

try:
    import pefile
    from unicorn import *
    from unicorn.x86_const import *
except ImportError:
    sys.exit("pip install pefile unicorn")

PAGE = 0x1000
STACK_BASE = 0x70000000
STACK_SIZE = 0x200000
SCRATCH_BASE = 0x60000000   # caller-provided scratch/output buffers
HEAP_BASE = 0x50000000      # fake allocator (when heap_stub=True)
HEAP_SIZE = 0x4000000
SENTINEL = 0x5EED_DEAD      # return address that stops emulation


def _align_down(x): return x & ~(PAGE - 1)
def _align_up(x):   return (x + PAGE - 1) & ~(PAGE - 1)


class Emu:
    def __init__(self, exe_path, default_stub_ret=0, trace=False, heap_stub=False):
        self.pe = pefile.PE(exe_path, fast_load=True)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        with open(exe_path, "rb") as f:
            self.data = f.read()
        self.default_stub_ret = default_stub_ret
        self.trace = trace
        # heap_stub: external (non-.text) calls return a fresh writable heap block
        # instead of 0, so malloc/std::string paths don't null-deref.
        self.heap_stub = heap_stub
        self.heap = HEAP_BASE
        self.stub_rets = {}     # va -> forced EAX for specific external calls
        self.intercepts = {}    # va -> label: record args + emulate a return
        self.intercept_cleanup = {}  # va -> stdcall arg bytes the callee pops
        self.trace_calls = []   # recorded (label, ecx, edx, arg0, arg1)
        self.mapped = []        # (start, end) of mapped exec sections
        self.text_range = None
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        self._enable_fpu_sse()
        self._map_image()
        self._map_region(STACK_BASE, STACK_SIZE)
        self._map_region(SCRATCH_BASE, 0x100000)
        if heap_stub:
            self._map_region(HEAP_BASE, HEAP_SIZE)
        self._install_hooks()

    def _enable_fpu_sse(self):
        """Unicorn boots with SSE disabled; real MSVC code (std::string, sprintf,
        float fmt) uses SSE. Clear CR0.EM, set CR0.MP, set CR4.OSFXSR/OSXMMEXCPT."""
        cr0 = self.uc.reg_read(UC_X86_REG_CR0)
        self.uc.reg_write(UC_X86_REG_CR0, (cr0 & ~(1 << 2)) | (1 << 1))
        cr4 = self.uc.reg_read(UC_X86_REG_CR4)
        self.uc.reg_write(UC_X86_REG_CR4, cr4 | (1 << 9) | (1 << 10))

    # ---- memory setup -------------------------------------------------
    def _map_region(self, addr, size):
        addr = _align_down(addr); size = _align_up(size)
        self.uc.mem_map(addr, size)
        return addr, size

    def _map_image(self):
        for s in self.pe.sections:
            va = self.base + s.VirtualAddress
            vsize = max(s.Misc_VirtualSize, s.SizeOfRawData)
            start = _align_down(va)
            end = _align_up(va + vsize)
            self.uc.mem_map(start, end - start)
            raw = self.data[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
            self.uc.mem_write(va, raw)
            name = s.Name.rstrip(b"\x00")
            if name == b".text":
                self.text_range = (va, va + s.Misc_VirtualSize)
            self.mapped.append((start, end))

    # ---- hooks --------------------------------------------------------
    def _in_text(self, addr):
        lo, hi = self.text_range
        return lo <= addr < hi

    def _install_hooks(self):
        def hook_code(uc, address, size, _):
            if self.trace and self._in_text(address):
                print(f"  exec {address:#010x}")
            # Intercepted in-code routine. A string label just records args and
            # returns 1; a callable runs custom logic (e.g. feed JSON bytes) and
            # its return value becomes EAX. Either way we emulate a return.
            if address in self.intercepts:
                esp = uc.reg_read(UC_X86_REG_ESP)
                a0, a1 = struct.unpack("<II", uc.mem_read(esp + 4, 8))
                ecx = uc.reg_read(UC_X86_REG_ECX)
                h = self.intercepts[address]
                if callable(h):
                    eax = h(uc, ecx, a0, a1) or 0
                else:
                    self.trace_calls.append((h, ecx, uc.reg_read(UC_X86_REG_EDX), a0, a1))
                    eax = 1
                ret = struct.unpack("<I", uc.mem_read(esp, 4))[0]
                uc.reg_write(UC_X86_REG_ESP, esp + 4 + self.intercept_cleanup.get(address, 0))
                uc.reg_write(UC_X86_REG_EAX, eax)
                uc.reg_write(UC_X86_REG_EIP, ret)
                return
            # A CALL that left .text -> external/import/garbage. Emulate a near
            # RET: pop return address, force EAX, resume at caller.
            if not self._in_text(address):
                esp = uc.reg_read(UC_X86_REG_ESP)
                ret = struct.unpack("<I", uc.mem_read(esp, 4))[0]
                uc.reg_write(UC_X86_REG_ESP, esp + 4)
                if address in self.stub_rets:
                    eax = self.stub_rets[address]
                elif self.heap_stub:
                    eax = self.heap; self.heap += 0x800   # fresh writable block
                else:
                    eax = self.default_stub_ret
                uc.reg_write(UC_X86_REG_EAX, eax)
                uc.reg_write(UC_X86_REG_EIP, ret)
        self.uc.hook_add(UC_HOOK_CODE, hook_code)

        def hook_unmapped(uc, access, address, size, value, _):
            page = _align_down(address)
            try:
                uc.mem_map(page, PAGE)
                return True   # retry the access against fresh zero page
            except UcError:
                return False
        self.uc.hook_add(UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED
                         | UC_HOOK_MEM_FETCH_UNMAPPED, hook_unmapped)

    # ---- public API ---------------------------------------------------
    def write(self, addr, data: bytes): self.uc.mem_write(addr, data)
    def read(self, addr, n): return bytes(self.uc.mem_read(addr, n))

    def call(self, func_va, args=None, ecx=None, timeout_s=5, max_insn=2_000_000):
        """Call func with cdecl args (list of ints). Set `ecx` for thiscall
        (the `this` pointer). Returns EAX. Sentinel stops the run."""
        args = args or []
        esp = STACK_BASE + STACK_SIZE - 0x1000
        for a in reversed(args):
            esp -= 4; self.uc.mem_write(esp, struct.pack("<I", a & 0xFFFFFFFF))
        esp -= 4; self.uc.mem_write(esp, struct.pack("<I", SENTINEL))
        self.uc.reg_write(UC_X86_REG_ESP, esp)
        self.uc.reg_write(UC_X86_REG_EBP, esp)
        if ecx is not None:
            self.uc.reg_write(UC_X86_REG_ECX, ecx)
        # map a 1-page landing for the sentinel so the fetch hook can stop us
        try:
            self.uc.mem_map(_align_down(SENTINEL), PAGE)
        except UcError:
            pass
        try:
            self.uc.emu_start(func_va, SENTINEL, timeout=timeout_s * 1_000_000,
                              count=max_insn)
        except UcError as e:
            eip = self.uc.reg_read(UC_X86_REG_EIP)
            if eip != SENTINEL:
                raise RuntimeError(f"emu fault at {eip:#x}: {e}")
        return self.uc.reg_read(UC_X86_REG_EAX)


def _self_test(exe):
    e = Emu(exe)
    print(f"[+] image mapped, base={e.base:#x}, .text={e.text_range[0]:#x}-{e.text_range[1]:#x}")
    print(f"[+] {len(e.mapped)} sections mapped into Unicorn")
    print("[+] harness ready — import Emu and call(func_va, args) on a target routine")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("exe", nargs="?", default="MightyQuest_unpacked_fixed (1).exe")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        _self_test(a.exe)
    else:
        print(__doc__)
