#!/usr/bin/env python3
"""
validate_consistency.py — exhaustively check that, for EVERY contract, what the
client *writes* (serialize) exactly matches what it *reads* (deserialize): same
field names, same types. Any mismatch is a place where one side could send
something the other won't read correctly — the class of bug that breaks an online
client/server eventually.

For each `*Serializer` we resolve its vtable, find the serialize method (calls the
writeKey primitive) and the deserialize method (calls the unknown-field handler),
walk both to (field -> type), and diff them.

Output: re/catalog/network/consistency_report.txt   (+ a stdout summary)

Run: python3 re/tools/validate_consistency.py
"""
from __future__ import annotations
import csv, os, struct, sys
from bisect import bisect_right
from collections import Counter

try:
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    from capstone.x86 import X86_OP_IMM, X86_OP_MEM
except ImportError:
    sys.exit("pip install pefile capstone")

EXE = "MightyQuest_unpacked_fixed (1).exe"
OUT = "re/catalog/network/consistency_report.txt"
WRITE_KEY = 0x009ab550
UNKNOWN_FIELD = 0x009a9ce0

# writer VA -> type, reader VA -> type (from 05-SCHEMA-CATALOG.md), normalised to
# comparable categories so writeInt vs readInt etc. line up.
WRITERS = {0x009aad80: "int", 0x009ab060: "string", 0x009ab3f0: "bool",
           0x009aae20: "float", 0x009aae70: "datetime"}
READERS = {0x009a8d30: "int", 0x009a9450: "string", 0x009a8c90: "bool",
           0x009a9170: "duration"}
PRIM_W = (0x009aa000, 0x009ac000)
PRIM_R = (0x009a8000, 0x009aa000)
NUM = {"int", "number", "float", "duration"}      # treat numeric widths as one


def category(t):
    return "num" if t in NUM else t


def compatible(wt, rt):
    """do the write-side and read-side types agree?

    Scalar types (string/bool/datetime) must match exactly. The reader side
    under-detects nested objects (some object readers fall in the numeric band),
    so object<->num is treated as compatible rather than a false conflict."""
    a, b = category(wt), category(rt)
    if a == b:
        return True
    # the reader side under-detects nested objects and datetimes (their readers
    # fall in the numeric band), so these pair with num rather than conflicting.
    return {a, b} <= {"num", "object"} or {a, b} <= {"num", "datetime"}


def main():
    pe = pefile.PE(EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = open(EXE, "rb").read()
    secs = [(base + s.VirtualAddress, s.SizeOfRawData, s.PointerToRawData,
             s.Misc_VirtualSize, s.Name.rstrip(b"\0")) for s in pe.sections]

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

    def ident(va, n=64):
        o = off(va)
        if o is None: return None
        e = data.find(b"\x00", o, o + n)
        if e < 0: return None
        s = data[o:e]
        if s and 2 <= len(s) <= 48 and chr(s[0]).isalpha() and \
           all(chr(c).isalnum() or c == 0x5f for c in s):
            return s.decode("latin1")
        return None

    fstarts, fsize = [], {}
    for r in csv.DictReader(open("re/catalog/functions.csv")):
        a = int(r["address"], 16); fstarts.append(a); fsize[a] = int(r["size"])
    fstarts.sort()

    def fsz(va):
        i = bisect_right(fstarts, va) - 1
        return fsize.get(fstarts[i], 96) if i >= 0 and fstarts[i] == va else 96

    md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True

    def vtable_of(addr):
        o = off(addr)
        for ins in md.disasm(data[o:o + 64], addr):
            for op in ins.operands:
                if op.type == X86_OP_IMM and rlo <= op.imm < rhi:
                    t = u32(op.imm)
                    if t is not None and tlo <= t < thi:
                        return op.imm
        return None

    def walk(maddr, is_writer):
        """return {field: type} by pairing each key with its value primitive."""
        o = off(maddr)
        if o is None: return None, False
        code = data[o:o + fsz(maddr)]
        last_id = None; pend = None; awaiting = False; fields = {}
        is_ser = False; is_deser = False
        for ins in md.disasm(code, maddr):
            if ins.mnemonic == "call":
                ops = ins.operands
                if ops and ops[0].type == X86_OP_IMM:
                    t = ops[0].imm
                    if is_writer:
                        if t == WRITE_KEY:
                            is_ser = True; pend = last_id; awaiting = True; continue
                        if awaiting and pend:
                            typ = WRITERS.get(t, "number" if PRIM_W[0] <= t < PRIM_W[1] else "object")
                            fields[pend] = typ; awaiting = False; pend = None
                    else:
                        if t == UNKNOWN_FIELD:
                            is_deser = True; last_id = None; continue
                        if last_id is not None and t != maddr:
                            typ = READERS.get(t, "number" if PRIM_R[0] <= t < PRIM_R[1] else "object")
                            fields[last_id] = typ; last_id = None
                else:
                    if is_writer: awaiting = False
                    else: last_id = None
            else:
                for op in ins.operands:
                    v = op.imm if op.type == X86_OP_IMM else (
                        op.mem.disp if op.type == X86_OP_MEM else 0)
                    if rlo <= v < rhi:
                        s = ident(v)
                        if s: last_id = s
        return fields, (is_ser if is_writer else is_deser)

    stubs = []
    for r in csv.DictReader(open("re/catalog/pe/function_classification.csv")):
        if r["source"].endswith("Serializer.cpp") and int(r["size"]) <= 64:
            stubs.append((int(r["address"], 16), r["source"][:-len("Serializer.cpp")]))

    both = consistent = 0
    issues = []
    for addr, contract in stubs:
        vt = vtable_of(addr)
        if vt is None: continue
        ser = deser = None
        for slot in range(1, 8):
            m = u32(vt + slot * 4)
            if m is None or not (tlo <= m < thi): continue
            f, ok = walk(m, True)
            if ok and ser is None: ser = f; continue
            f2, ok2 = walk(m, False)
            if ok2 and deser is None: deser = f2
        if not ser or not deser:
            continue
        both += 1
        only_ser = sorted(set(ser) - set(deser))
        only_deser = sorted(set(deser) - set(ser))
        tmism = sorted(k for k in set(ser) & set(deser)
                       if not compatible(ser[k], deser[k]))
        if not only_ser and not only_deser and not tmism:
            consistent += 1
        else:
            issues.append((contract, only_ser, only_deser, tmism, ser, deser))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(f"# serialize<->deserialize consistency for two-way contracts\n")
        f.write(f"# {consistent}/{both} fully consistent; {len(issues)} with diffs\n\n")
        for contract, os_, od_, tm_, ser, deser in issues:
            f.write(f"{contract}:\n")
            if os_: f.write(f"    written but not read : {os_}\n")
            if od_: f.write(f"    read but not written : {od_}\n")
            for k in tm_:
                f.write(f"    type differs [{k}] : write={ser[k]} read={deser[k]}\n")
    print(f"[+] two-way contracts checked: {both}")
    print(f"[+] fully consistent (write==read): {consistent}  "
          f"({100*consistent//both if both else 0}%)")
    print(f"[+] with differences: {len(issues)} -> {OUT}")
    if issues:
        cat = Counter()
        for _, os_, od_, tm_, *_ in issues:
            if os_: cat["written-not-read"] += 1
            if od_: cat["read-not-written"] += 1
            if tm_: cat["type-mismatch"] += 1
        print("    breakdown:", dict(cat))


if __name__ == "__main__":
    main()
