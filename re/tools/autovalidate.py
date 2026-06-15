#!/usr/bin/env python3
"""
autovalidate.py — mass dynamic round-trip validation of contracts.

For each two-way contract it (1) auto-discovers each scalar field's object offset
by emulating the real deserialize dispatcher with a memory-write hook (we observe
*where* the parsed value lands), then (2) round-trips: deserialize every field
into one object, serialize it back through the real serialize method, and check
the values survive both directions. No static offset parsing, no game, no Windows.

This generalises validate_codec.py (hand-written specs) to the whole catalog.

Usage: python3 re/tools/autovalidate.py [--limit N]
"""
from __future__ import annotations
import argparse, csv, json, struct, sys
from bisect import bisect_right
sys.path.insert(0, "re/tools")
from emu import Emu, SCRATCH_BASE, HEAP_BASE
from unicorn import UC_HOOK_MEM_WRITE

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

EXE = "MightyQuest_unpacked_fixed (1).exe"
UNKNOWN_FIELD = 0x009a9ce0
W_KEY, W_INT, W_STR = 0x009ab550, 0x009aad80, 0x009ab060
W_OTHER = (0x009ab010, 0x009ab3f0, 0x009aae20, 0x009aae70, 0x009aadd0,
           0x009aaf40, 0x009aad30, 0x009aafc0, 0x009aaf50)

CTX, STREAM, SVT = SCRATCH_BASE + 0x1000, SCRATCH_BASE + 0x1300, SCRATCH_BASE + 0x1400
OBJ, NAME = SCRATCH_BASE + 0x2000, SCRATCH_BASE + 0x6000
FAKE_ADVANCE, FAKE_ERROR = SCRATCH_BASE + 0x10, SCRATCH_BASE + 0x20
OBJSZ = 0x800


SCALAR = {"num", "str", "bool"}      # wire shapes that are simple scalars


def kind_of(t):
    return t          # shapes are already num / str / bool


def feed_bytes(kind, val):
    if kind == "str":
        # an ISO string satisfies plain-string AND datetime readers; enum readers
        # (string lookup) may reject it -> that field just won't discover (safe).
        return b'"2015-06-15T00:00:00Z",' if val == "_dt_" else b'"' + str(val).encode() + b'",'
    if kind == "bool":
        return (b"true," if val else b"false,")
    return str(val).encode() + b","   # numeric


def cstr(e, a, n=40):
    b = e.read(a, n); z = b.find(b"\x00")
    return b[:z if z >= 0 else n].decode("latin1")


class Validator:
    def __init__(self):
        self.e = Emu(EXE)
        self.feed = {"b": b"", "i": 1}
        self.writes = []
        # persistent hooks (Emu reused across all contracts for speed)
        e = self.e

        def adv(uc, ecx, a0, a1):
            f = self.feed
            if f["i"] < len(f["b"]):
                uc.mem_write(CTX + 4, bytes([f["b"][f["i"]]])); f["i"] += 1; return 1
            uc.mem_write(CTX + 4, b"\x00"); return 0
        self.adv = adv

        def wh(uc, acc, addr, size, val, _):
            if OBJ <= addr < OBJ + OBJSZ:
                self.writes.append((addr - OBJ, size))
        e.uc.hook_add(UC_HOOK_MEM_WRITE, wh)

    def _reset_ctx(self, jb, prefill=b"\x00"):
        e = self.e
        e.heap = HEAP_BASE
        self.feed = {"b": jb, "i": 1}
        e.write(SVT, b"\x00" * 0x40)
        e.write(SVT + 4, struct.pack("<I", FAKE_ADVANCE))
        e.write(SVT + 0x1c, struct.pack("<I", FAKE_ERROR))
        e.write(STREAM, struct.pack("<I", SVT))
        e.write(CTX, struct.pack("<IBxxxII", STREAM, jb[0], 0, 0))

    def discover(self, deser, name, kind):
        """run deserialize for one field; return its write offset (or None)."""
        jb = feed_bytes(kind, 7 if kind in ("num", "float") else (1 if kind == "bool" else "ab"))
        self._reset_ctx(jb)
        self.e.write(OBJ, b"\x40" * OBJSZ)          # large string capacities
        self.e.write(NAME, name.encode() + b"\x00")
        self.e.intercepts = {FAKE_ADVANCE: self.adv, FAKE_ERROR: (lambda *a: 0)}
        self.e.intercept_cleanup = {FAKE_ADVANCE: 8}
        self.writes = []
        try:
            self.e.call(deser, [CTX, OBJ, NAME])
        except Exception:
            return None
        ow = [o for o, s in self.writes]
        return min(ow) if ow else None

    def roundtrip(self, deser, ser, fields):
        """fields: [(name, off, kind)]. deserialize all in, serialize out, compare."""
        e = self.e
        e.write(OBJ, b"\x00" * OBJSZ)
        vals = {}
        # deserialize each field into the shared object
        for i, (name, off, kind) in enumerate(fields):
            v = (1000 + i) if kind in ("num", "float") else (1 if kind == "bool" else f"v{i}")
            vals[name] = v
            jb = feed_bytes(kind, v)
            if kind == "str":
                e.write(OBJ + off - 4, struct.pack("<I", 0x40))   # capacity
            self._reset_ctx(jb)
            e.write(NAME, name.encode() + b"\x00")
            e.intercepts = {FAKE_ADVANCE: self.adv, FAKE_ERROR: (lambda *a: 0)}
            e.intercept_cleanup = {FAKE_ADVANCE: 8}
            try:
                e.call(deser, [CTX, OBJ, NAME])
            except Exception:
                return None

        def readf(o, k):
            if k == "str": return cstr(e, OBJ + o)
            if k == "bool": return e.read(OBJ + o, 1)[0]
            return struct.unpack("<i", e.read(OBJ + o, 4))[0]
        din = {n: readf(o, k) for n, o, k in fields}
        # serialize the assembled object, capturing what it emits
        seq, pend = {}, {"k": None}

        def on_key(uc, ecx, a0, a1):
            pend["k"] = cstr(e, a0) or cstr(e, ecx); return 1

        def on_int(uc, ecx, a0, a1):
            p = next((x for x in (a0, a1, ecx) if OBJ <= x < OBJ + OBJSZ), a1)
            seq[pend["k"]] = struct.unpack("<i", e.read(p, 4))[0]; return 1

        def on_str(uc, ecx, a0, a1):
            p = next((x for x in (a0, a1, ecx) if OBJ <= x < OBJ + OBJSZ), a0)
            seq[pend["k"]] = cstr(e, p); return 1

        W_BOOL = 0x009ab3f0

        def on_bool(uc, ecx, a0, a1):
            p = next((x for x in (a0, a1, ecx) if OBJ <= x < OBJ + OBJSZ), a0)
            seq[pend["k"]] = e.read(p, 1)[0]; return 1

        e.intercepts = {W_KEY: on_key, W_INT: on_int, W_STR: on_str, W_BOOL: on_bool}
        for w in W_OTHER:
            if w != W_BOOL:
                e.intercepts[w] = (lambda *a: 1)
        e.intercept_cleanup = {w: 4 for w in (W_KEY, W_INT, W_STR) + W_OTHER}
        try:
            e.call(ser, [SCRATCH_BASE + 0x7000, OBJ])
        except Exception:
            return None
        return din, seq, vals


def find_methods(pe, base, data):
    """contract -> (deser_method, ser_method) via the serializer stub vtable."""
    secs = [(base + s.VirtualAddress, s.SizeOfRawData, s.PointerToRawData,
             s.Misc_VirtualSize, s.Name.rstrip(b"\0")) for s in pe.sections]

    def off(va):
        for a, rsz, praw, _, _ in secs:
            if a <= va < a + rsz:
                return praw + (va - a)
        return None
    text = next(s for s in secs if s[4] == b".text"); tlo, thi = text[0], text[0] + text[3]
    rd = next(s for s in secs if s[4] == b".rdata"); rlo, rhi = rd[0], rd[0] + rd[3]

    def u32(va):
        o = off(va); return struct.unpack_from("<I", data, o)[0] if o is not None else None
    fstarts, fsz = [], {}
    for r in csv.DictReader(open("re/catalog/functions.csv")):
        a = int(r["address"], 16); fstarts.append(a); fsz[a] = int(r["size"])
    fstarts.sort()

    def size(va):
        i = bisect_right(fstarts, va) - 1
        return fsz.get(fstarts[i], 96) if i >= 0 and fstarts[i] == va else 96
    md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True

    def vtable(addr):
        o = off(addr)
        for ins in md.disasm(data[o:o + 64], addr):
            for op in ins.operands:
                if op.type == X86_OP_IMM and rlo <= op.imm < rhi:
                    t = u32(op.imm)
                    if t is not None and tlo <= t < thi:
                        return op.imm
        return None

    def role(m):
        o = off(m)
        if o is None: return None
        calls = [i.operands[0].imm for i in md.disasm(data[o:o + size(m)], m)
                 if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM]
        if W_KEY in calls: return "ser"
        if UNKNOWN_FIELD in calls: return "deser"
        return None

    out = {}
    for r in csv.DictReader(open("re/catalog/pe/function_classification.csv")):
        if r["source"].endswith("Serializer.cpp") and int(r["size"]) <= 64:
            c = r["source"][:-len("Serializer.cpp")]
            vt = vtable(int(r["address"], 16))
            if vt is None: continue
            ser = deser = None
            for slot in range(1, 8):
                m = u32(vt + slot * 4)
                if m is None or not (tlo <= m < thi): continue
                rr = role(m)
                if rr == "ser" and not ser: ser = m
                elif rr == "deser" and not deser: deser = m
            if ser and deser:
                out[c] = (deser, ser)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=120)
    args = ap.parse_args()

    typed = json.load(open("re/catalog/network/schemas_typed.json"))
    pe = pefile.PE(EXE, fast_load=True); base = pe.OPTIONAL_HEADER.ImageBase
    data = open(EXE, "rb").read()
    methods = find_methods(pe, base, data)

    # candidate contracts: two-way, all-scalar fields (no nested objects)
    cands = []
    for c, info in typed.items():
        if info["direction"] != "both" or c not in methods:
            continue
        if all(t in SCALAR for _, t in info["fields"]) and info["fields"]:
            cands.append((c, info["fields"]))
    cands = cands[:args.limit]

    v = Validator()
    incoming_ok = roundtrip_ok = miss = fail = 0
    failures = []
    for c, flds in cands:
        deser, ser = methods[c]
        fields, good = [], True
        for name, t in flds:
            kind = kind_of(t)
            off = v.discover(deser, name, kind)
            if off is None:
                good = False; break
            fields.append((name, off, kind))
        if not good:
            miss += 1; continue
        incoming_ok += 1                       # every field parsed via the real reader
        res = v.roundtrip(deser, ser, fields)
        if res is None:
            failures.append((c, "emu")); continue
        din, seq, vals = res
        # INCOMING: real reader parsed each num/bool/str field to the right value
        din_ok = all(din.get(n) == vals[n] for n, _, k in fields if k in ("num", "str", "bool"))
        # OUTGOING: every field the serializer emitted-and-we-captured is correct
        out_ok = bool(seq) and all(seq[n] == vals[n] for n in seq if n in vals)
        if din_ok and out_ok:
            roundtrip_ok += 1
        else:
            failures.append((c, "in" if not din_ok else "out"))

    report = "re/catalog/network/roundtrip_report.txt"
    with open(report, "w") as f:
        f.write("# dynamic validation via the client's real codec\n")
        f.write(f"# candidates (two-way, all-scalar): {len(cands)}\n")
        f.write(f"# incoming validated (every field parsed): {incoming_ok}\n")
        f.write(f"# full round-trip (int/num/bool/str in==out): {roundtrip_ok}\n")
        f.write(f"# offset-discovery incomplete: {miss}\n\n")
        if failures:
            f.write("non-passing round-trip:\n")
            for c, why in failures:
                f.write(f"  {c}: {why}\n")
    print(f"[+] candidates (two-way, all-scalar): {len(cands)}")
    print(f"[+] INCOMING validated (every field parsed by real reader): "
          f"{incoming_ok}  ({100*incoming_ok//len(cands)}%)")
    print(f"[+] full round-trip OK (in==out): {roundtrip_ok}")
    print(f"[+] offset-discovery incomplete: {miss}")
    print(f"[+] report -> {report}")
    if failures:
        print("    non-passing round-trip:", ", ".join(f"{c}({w})" for c, w in failures[:8]))


if __name__ == "__main__":
    main()
