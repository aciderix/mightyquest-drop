#!/usr/bin/env python3
"""
extract_schemas.py — Automatically recover the JSON schema of every serializable
contract in the client.

Pipeline (no manual step, no Ghidra needed):
  1. Each `*Serializer` registration stub (labeled in function_classification.csv)
     stores its vtable pointer. We disassemble the tiny stub to find that vtable.
  2. The vtable holds the serialize/deserialize method pointers (into .text).
  3. We scan each method's byte range for 4-byte words that reference an ASCII
     string in .rdata — those referenced strings are the JSON field keys.
  4. The contract name comes for free from the stub's source label
     (`FooSerializer.cpp` -> contract `Foo`).

Output: re/catalog/network/schemas.json  { contract: [field, ...], ... }
        re/catalog/network/schemas.txt   human-readable

Usage: python3 re/tools/extract_schemas.py
"""
from __future__ import annotations
import csv, json, os, re, struct, sys
from bisect import bisect_right

try:
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    from capstone.x86 import X86_OP_IMM
except ImportError:
    sys.exit("pip install pefile capstone")

EXE = "MightyQuest_unpacked_fixed (1).exe"
FUNCS = "re/catalog/functions.csv"
OUTDIR = "re/catalog/network"
SHARED_BASE_METHOD = 0x006e0440      # vtable slot 0 shared by all serializers
KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{1,48}$")


def main():
    pe = pefile.PE(EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = open(EXE, "rb").read()

    secs = [(base + s.VirtualAddress, s.SizeOfRawData, s.PointerToRawData,
             s.Name.rstrip(b"\0")) for s in pe.sections]

    def va_to_off(va):
        for a, rsz, praw, _ in secs:
            if a <= va < a + rsz:
                return praw + (va - a)
        return None

    text = next(s for s in pe.sections if s.Name.rstrip(b"\0") == b".text")
    tlo, thi = base + text.VirtualAddress, base + text.VirtualAddress + text.Misc_VirtualSize
    rdata = next(s for s in pe.sections if s.Name.rstrip(b"\0") == b".rdata")
    rlo, rhi = base + rdata.VirtualAddress, base + rdata.VirtualAddress + rdata.Misc_VirtualSize

    def read_u32(va):
        off = va_to_off(va)
        return struct.unpack_from("<I", data, off)[0] if off is not None else None

    def cstr_at(va, maxlen=64):
        off = va_to_off(va)
        if off is None:
            return None
        end = data.find(b"\x00", off, off + maxlen)
        if end < 0:
            return None
        s = data[off:end]
        return s.decode("latin1") if s and all(32 <= c < 127 for c in s) else None

    # function start -> size  (for bounding method byte ranges)
    fstarts, fsize = [], {}
    with open(FUNCS, newline="") as f:
        for r in csv.DictReader(f):
            a = int(r["address"], 16); fstarts.append(a); fsize[a] = int(r["size"])
    fstarts.sort()

    def func_size(va):
        i = bisect_right(fstarts, va) - 1
        return fsize.get(fstarts[i], 64) if i >= 0 and fstarts[i] == va else 64

    # serializer registration stubs: address + contract name
    stubs = []
    with open("re/catalog/pe/function_classification.csv", newline="") as f:
        for r in csv.DictReader(f):
            src = r["source"]
            if src.endswith("Serializer.cpp") and int(r["size"]) <= 64:
                contract = src[:-len("Serializer.cpp")]
                stubs.append((int(r["address"], 16), contract))

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True

    def vtable_of_stub(addr):
        """find the vtable VA the stub stores (a .rdata ptr whose target is .text)."""
        code = data[va_to_off(addr):va_to_off(addr) + 64]
        for insn in md.disasm(code, addr):
            for o in insn.operands:
                if o.type == X86_OP_IMM and rlo <= o.imm < rhi:
                    tgt = read_u32(o.imm)
                    if tgt is not None and tlo <= tgt < thi:
                        return o.imm
        return None

    def keys_in_method(maddr):
        size = func_size(maddr)
        off = va_to_off(maddr)
        if off is None:
            return []
        body = data[off:off + size]
        found = []
        for i in range(0, len(body) - 4):
            w = body[i] | (body[i+1] << 8) | (body[i+2] << 16) | (body[i+3] << 24)
            if rlo <= w < rhi:
                s = cstr_at(w)
                if s and KEY_RE.match(s):
                    found.append(s)
        return found

    schemas = {}
    for addr, contract in stubs:
        vt = vtable_of_stub(addr)
        if vt is None:
            continue
        keys = []
        for slot in range(1, 8):                 # slot 0 is the shared base method
            m = read_u32(vt + slot * 4)
            if m is None or not (tlo <= m < thi) or m == SHARED_BASE_METHOD:
                continue
            keys += keys_in_method(m)
        # dedup, drop the contract's own type name and obvious noise
        seen, fields = set(), []
        for k in keys:
            if k in seen or k == contract:
                continue
            seen.add(k); fields.append(k)
        if fields:
            schemas[contract] = fields

    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "schemas.json"), "w") as f:
        json.dump(schemas, f, indent=1, sort_keys=True)
    with open(os.path.join(OUTDIR, "schemas.txt"), "w") as f:
        for c in sorted(schemas):
            f.write(f"{c}: {{ {', '.join(schemas[c])} }}\n")

    nkeys = sum(len(v) for v in schemas.values())
    print(f"[+] {len(stubs)} serializer stubs scanned")
    print(f"[+] {len(schemas)} contracts with recovered fields ({nkeys} fields total)")
    print(f"[+] -> {OUTDIR}/schemas.json, schemas.txt")


if __name__ == "__main__":
    main()
