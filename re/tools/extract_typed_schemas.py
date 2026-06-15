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
UNKNOWN_FIELD = 0x009a9ce0       # called by every deserialize method (its marker)

# Exact per-primitive WIRE SHAPE — what the field looks like on the wire. This is
# what makes a message well-formed: a bare number, a quoted string, true/false,
# an array, or a nested object. (Numeric width — int/uint/byte/long/double — is
# recorded for value validity but all share the `num` wire shape.) Identified by
# decompiling every scalar writer/reader (see 05-SCHEMA-CATALOG.md):
#   buffer widths 4/11/12/22/20 -> byte/uint/int/int64/double; "false" -> bool;
#   ISO format -> datetime(quoted); enum writes/reads a quoted name; readers with
#   a ']' branch -> array.
W_SHAPE = {
    0x009aad80: "num", 0x009aadd0: "num", 0x009aad30: "num", 0x009aafc0: "num",
    0x009ab010: "num", 0x009aae20: "num", 0x009aaf40: "num", 0x009aaf50: "num",
    0x009aaf30: "num", 0x009aaf60: "num", 0x009aaf70: "num",
    0x009ab060: "str", 0x009aae70: "str", 0x009aaf00: "str",   # string/datetime/enum
    0x009ab3f0: "bool",
}
R_SHAPE = {
    0x009a8d30: "num", 0x009a8d40: "num", 0x009a9390: "num",
    0x009a9170: "num", 0x009a9440: "num", 0x009a8d20: "num", 0x009a93a0: "num",
    0x009a9410: "num", 0x009a93b0: "num", 0x009a98a0: "arr",
    0x009a9450: "str", 0x009a9b10: "str", 0x009a8670: "str", 0x009a8e70: "str",
    0x009a8f90: "str",   # datetime reader (parses the quoted ISO-8601 string)
    0x009a8c90: "bool", 0x009a99d0: "arr", 0x009a9680: "obj",
}
W_BAND, R_BAND = (0x009aa000, 0x009ac000), (0x009a8000, 0x009aa000)


def writer_shape(va):
    if va in W_SHAPE: return W_SHAPE[va]
    return "num" if W_BAND[0] <= va < W_BAND[1] else "obj"


def reader_shape(va):
    if va in R_SHAPE: return R_SHAPE[va]
    return "num" if R_BAND[0] <= va < R_BAND[1] else "obj"

# writer primitive VA -> field type. Identified by decompiling each primitive
# (see 05-SCHEMA-CATALOG.md): bool writes "false", datetime uses an ISO-8601
# format, float's formatter handles "toobig", etc. Scalar JSON primitives live
# in the 0x009aa000-0x009ac000 band; writers outside it are per-contract
# generated object/array writers (nested values).
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

    def walk_deserialize(maddr):
        """return ordered [(key, type)] for a deserialize method (marked by a
        call to UNKNOWN_FIELD). Each key is paired with the next reader call."""
        o = off(maddr)
        if o is None: return None
        code = data[o:o + fsz(maddr)]
        last_ident = None
        pairs = []
        is_deser = False
        for insn in md.disasm(code, maddr):
            if insn.mnemonic == "call":
                ops = insn.operands
                if ops and ops[0].type == X86_OP_IMM:
                    tgt = ops[0].imm
                    if tgt == UNKNOWN_FIELD:
                        is_deser = True; last_ident = None; continue
                    if last_ident is not None and tgt != maddr:
                        pairs.append((last_ident, reader_shape(tgt)))
                        last_ident = None
                else:
                    last_ident = None
            else:
                for op in insn.operands:
                    if op.type == X86_OP_IMM and rlo <= op.imm < rhi:
                        s = ident_at(op.imm)
                        if s: last_ident = s
                    elif op.type == X86_OP_MEM and op.mem.disp and rlo <= op.mem.disp < rhi:
                        s = ident_at(op.mem.disp)
                        if s: last_ident = s
        return pairs if is_deser else None

    # collect serializer stubs (addr, contract)
    stubs = []
    with open("re/catalog/pe/function_classification.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["source"].endswith("Serializer.cpp") and int(r["size"]) <= 64:
                stubs.append((int(r["address"], 16), r["source"][:-len("Serializer.cpp")]))

    writer_freq = Counter()
    ser, deser = {}, {}        # contract -> [(key, type)]
    for addr, contract in stubs:
        vt = vtable_of(addr)
        if vt is None: continue
        for slot in range(1, 8):
            m = u32(vt + slot * 4)
            if m is None or not (tlo <= m < thi): continue
            sp = walk_serialize(m)
            if sp:
                fields = [[k, writer_shape(w)] for k, w in sp if k != contract]
                for _, w in sp: writer_freq[w] += 1
                if fields: ser[contract] = fields
                continue
            dp = walk_deserialize(m)
            if dp:
                fields = [[k, t] for k, t in dp if k != contract]
                if fields: deser.setdefault(contract, fields)

    if args.discover:
        print("Top writer primitives (addr: count) — name these in WRITERS:")
        for w, c in writer_freq.most_common(25):
            print(f"  0x{w:08x}  {c:6d}  {writer_shape(w)}")
        return

    # merge: prefer serialize fields (richer types: datetime/float); attach a
    # protocol direction so a server author knows who emits each message.
    contracts = set(ser) | set(deser)
    merged = {}
    for c in contracts:
        if c in ser and c in deser:
            direction, fields = "both", ser[c]
        elif c in ser:
            direction, fields = "request", ser[c]
        else:
            direction, fields = "response", deser[c]
        merged[c] = {"direction": direction, "fields": fields}

    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "schemas_typed.json"), "w") as f:
        json.dump(merged, f, indent=1, sort_keys=True)
    with open(os.path.join(OUTDIR, "schemas_typed.txt"), "w") as f:
        for c in sorted(merged):
            inner = ", ".join(f"{k}: {t}" for k, t in merged[c]["fields"])
            f.write(f"[{merged[c]['direction']:8}] {c} {{ {inner} }}\n")

    dirc = Counter(v["direction"] for v in merged.values())
    tc = Counter(t for v in merged.values() for _, t in v["fields"])
    total = sum(len(v["fields"]) for v in merged.values())
    print(f"[+] {len(merged)} contracts, {total} typed fields")
    print("    direction:", dict(dirc))
    print("    types:", dict(tc.most_common()))
    print(f"[+] -> {OUTDIR}/schemas_typed.json, schemas_typed.txt")


if __name__ == "__main__":
    main()
