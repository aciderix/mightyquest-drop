#!/usr/bin/env python3
"""
extract_typed_schemas.py — add field TYPES to the contract schemas.

In each contract's *serialize* method the pattern is, per field:
    writeKey("FieldName"); write<Type>(&value)
So by disassembling the serialize method and pairing each writeKey call with the
*next* call (the value writer), we learn the type of every field. The writer
function addresses are mapped to type names in WRITERS below (seeded from the
hand-reversed login slice, extended by --discover).

Usage:
  python3 re/tools/extract_typed_schemas.py --discover   # rank writer prims
  python3 re/tools/extract_typed_schemas.py              # emit typed schemas
"""
from __future__ import annotations
import argparse, csv, json, os, struct, sys
from bisect import bisect_right
from collections import Counter

try:
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    from capstone.x86 import X86_OP_IMM, X86_OP_MEM
except ImportError:
    sys.exit("pip install pefile capstone")

EXE = "MightyQuest_unpacked_fixed (1).exe"
OUTDIR = "re/catalog/network"
WRITE_KEY = 0x009ab550

# writer primitive VA -> field type. Identified by decompiling each primitive
# (see 05-SCHEMA-CATALOG.md): bool writes "false", datetime uses an ISO-8601
# format, float's formatter handles "toobig", etc. Scalar JSON primitives live
# in the 0x009aa000-0x009ac000 band; writers outside it are per-contract
# generated object/array writers (nested values).
WRITERS = {
    0x009aad80: "int",
    0x009ab060: "string",
    0x009ab3f0: "bool",
    0x009aae20: "float",
    0x009aae70: "datetime",
}
PRIM_LO, PRIM_HI = 0x009aa000, 0x009ac000


def type_of(writer_va):
    if writer_va in WRITERS:
        return WRITERS[writer_va]
    if PRIM_LO <= writer_va < PRIM_HI:
        return "number"          # numeric scalar, exact width unresolved
    return "object"              # nested object/array (per-contract writer)


def load_pe():
    pe = pefile.PE(EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = open(EXE, "rb").read()
    secs = [(base + s.VirtualAddress, s.SizeOfRawData, s.PointerToRawData,
             s.Misc_VirtualSize, s.Name.rstrip(b"\0")) for s in pe.sections]
    return pe, base, data, secs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--discover", action="store_true")
    args = ap.parse_args()

    pe, base, data, secs = load_pe()

    def off(va):
        for a, rsz, praw, _, _ in secs:
            if a <= va < a + rsz:
                return praw + (va - a)
        return None

    text = next(s for s in secs if s[4] == b".text")
    tlo, thi = text[0], text[0] + text[3]
    rdata = next(s for s in secs if s[4] == b".rdata")
    rlo, rhi = rdata[0], rdata[0] + rdata[3]

    def u32(va):
        o = off(va); return struct.unpack_from("<I", data, o)[0] if o is not None else None

    def ident_at(va, maxlen=64):
        o = off(va)
        if o is None: return None
        e = data.find(b"\x00", o, o + maxlen)
        if e < 0: return None
        s = data[o:e]
        if s and 2 <= len(s) <= 48 and all(32 <= c < 127 for c in s) \
           and (s[0:1].isalpha()) and all(chr(c).isalnum() or c == 0x5f for c in s):
            return s.decode("latin1")
        return None

    fstarts, fsize = [], {}
    with open("re/catalog/functions.csv", newline="") as f:
        for r in csv.DictReader(f):
            a = int(r["address"], 16); fstarts.append(a); fsize[a] = int(r["size"])
    fstarts.sort()

    def fsz(va):
        i = bisect_right(fstarts, va) - 1
        return fsize.get(fstarts[i], 96) if i >= 0 and fstarts[i] == va else 96

    md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True

    def vtable_of(addr):
        o = off(addr)
        for insn in md.disasm(data[o:o + 64], addr):
            for op in insn.operands:
                if op.type == X86_OP_IMM and rlo <= op.imm < rhi:
                    t = u32(op.imm)
                    if t is not None and tlo <= t < thi:
                        return op.imm
        return None

    def walk_serialize(maddr):
        """return ordered [(key, writer_va)] for a serialize method."""
        o = off(maddr)
        if o is None: return None
        code = data[o:o + fsz(maddr)]
        last_ident = None
        cur_key = None
        awaiting = False
        pairs = []
        is_serialize = False
        for insn in md.disasm(code, maddr):
            m = insn.mnemonic
            if m == "call":
                ops = insn.operands
                if ops and ops[0].type == X86_OP_IMM:
                    tgt = ops[0].imm
                    if tgt == WRITE_KEY:
                        is_serialize = True
                        cur_key = last_ident; awaiting = True
                        continue
                    if awaiting and cur_key:
                        pairs.append((cur_key, tgt)); awaiting = False; cur_key = None
                else:
                    if awaiting: awaiting = False
            else:
                for op in insn.operands:
                    if op.type == X86_OP_IMM and rlo <= op.imm < rhi:
                        s = ident_at(op.imm)
                        if s: last_ident = s
                    elif op.type == X86_OP_MEM and op.mem.disp and rlo <= op.mem.disp < rhi:
                        s = ident_at(op.mem.disp)
                        if s: last_ident = s
        return pairs if is_serialize else None

    # collect serializer stubs (addr, contract)
    stubs = []
    with open("re/catalog/pe/function_classification.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["source"].endswith("Serializer.cpp") and int(r["size"]) <= 64:
                stubs.append((int(r["address"], 16), r["source"][:-len("Serializer.cpp")]))

    writer_freq = Counter()
    typed = {}
    for addr, contract in stubs:
        vt = vtable_of(addr)
        if vt is None: continue
        for slot in range(1, 8):
            m = u32(vt + slot * 4)
            if m is None or not (tlo <= m < thi): continue
            pairs = walk_serialize(m)
            if pairs:
                fields = []
                for k, w in pairs:
                    if k == contract: continue
                    writer_freq[w] += 1
                    fields.append([k, type_of(w)])
                if fields:
                    typed[contract] = fields
                break

    if args.discover:
        print("Top writer primitives (addr: count) — name these in WRITERS:")
        for w, c in writer_freq.most_common(25):
            named = WRITERS.get(w, "?")
            print(f"  0x{w:08x}  {c:6d}  {named}")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "schemas_typed.json"), "w") as f:
        json.dump(typed, f, indent=1, sort_keys=True)
    with open(os.path.join(OUTDIR, "schemas_typed.txt"), "w") as f:
        for c in sorted(typed):
            inner = ", ".join(f"{k}: {t}" for k, t in typed[c])
            f.write(f"{c} {{ {inner} }}\n")
    from collections import Counter as _C
    tc = _C(t for fs in typed.values() for _, t in fs)
    total = sum(len(fs) for fs in typed.values())
    print(f"[+] {len(typed)} contracts, {total} fields")
    for t, n in tc.most_common():
        print(f"      {t:10} {n}")
    print(f"[+] -> {OUTDIR}/schemas_typed.json, schemas_typed.txt")


if __name__ == "__main__":
    main()
