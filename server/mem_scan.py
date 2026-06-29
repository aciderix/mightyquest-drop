#!/usr/bin/env python3
"""
mem_scan.py — scan the running game's memory for the tutorial creature objects.

The tutorial castle's CreatureTiers use distinctive 4-digit SpecContainerIds
(1081, 1057, 1028, 1029, 1003, 1001). Find those int32 values in the game's
committed memory; around each, the creature struct should hold the LEVEL (0x1e=30
right now). That gives the creature struct layout + level field offset, which is the
target for a hardware write-breakpoint to catch the level-setting code.

    python mem_scan.py --pid <pid> --value 1081
"""
import argparse, ctypes as C, struct, sys
from ctypes import wintypes

k32 = C.WinDLL("kernel32", use_last_error=True)
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400
MEM_COMMIT = 0x1000
PAGE_GUARD = 0x100
PAGE_NOACCESS = 0x01
READABLE = 0x02 | 0x04 | 0x20 | 0x40  # R, RW, RX, RWX


class MBI(C.Structure):
    _fields_ = [("BaseAddress", C.c_void_p), ("AllocationBase", C.c_void_p),
                ("AllocationProtect", wintypes.DWORD), ("RegionSize", C.c_size_t),
                ("State", wintypes.DWORD), ("Protect", wintypes.DWORD),
                ("Type", wintypes.DWORD)]


def regions(h):
    addr = 0
    mbi = MBI()
    while k32.VirtualQueryEx(h, C.c_void_p(addr), C.byref(mbi), C.sizeof(mbi)):
        size = mbi.RegionSize
        if (mbi.State == MEM_COMMIT and (mbi.Protect & READABLE)
                and not (mbi.Protect & (PAGE_GUARD | PAGE_NOACCESS))):
            yield mbi.BaseAddress or 0, size
        addr = (mbi.BaseAddress or 0) + size
        if addr >= 0x7FFF0000:
            break


def read(h, base, size):
    buf = (C.c_char * size)()
    got = C.c_size_t(0)
    if k32.ReadProcessMemory(h, C.c_void_p(base), buf, size, C.byref(got)):
        return buf.raw[:got.value]
    return b""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", type=int, required=True)
    ap.add_argument("--value", type=lambda x: int(x, 0), default=1081)
    ap.add_argument("--max-hits", type=int, default=12)
    a = ap.parse_args()
    h = k32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, a.pid)
    if not h:
        print("OpenProcess failed", C.get_last_error()); sys.exit(1)
    needle = struct.pack("<i", a.value)
    hits = 0
    for base, size in regions(h):
        if size > 64 * 1024 * 1024:
            continue
        data = read(h, base, size)
        off = data.find(needle)
        while off >= 0 and hits < a.max_hits:
            va = base + off
            # dump surrounding ints (-0x40..+0x60) to eyeball the struct + level(30)
            lo = max(0, off - 0x40)
            window = data[lo:off + 0x60]
            ints = struct.unpack_from("<%di" % (len(window) // 4), window, 0)
            has30 = any(v == 30 for v in ints)
            other = sum(1 for v in ints if v in (1057, 1028, 1029, 1003, 1001, 56, 57, 1))
            print("HIT %s @ 0x%X  (level-30 nearby:%s, other-specs:%d)"
                  % (a.value, va, has30, other))
            if has30 or other >= 1:
                base_int = (va - 0x40) & ~3
                print("   ints[-0x40..+0x60]:")
                for i, v in enumerate(ints):
                    mark = "  <== 30" if v == 30 else ("  <== spec" if v in (1057, 1028, 1029, 1003, 1001, 1081, 56, 57) else "")
                    print("     +0x%03x = %11d (0x%x)%s" % (lo + i * 4 - off, v, v & 0xFFFFFFFF, mark))
            hits += 1
            off = data.find(needle, off + 1)
        if hits >= a.max_hits:
            break
    print("total hits:", hits)
    k32.CloseHandle(h)


if __name__ == "__main__":
    main()
