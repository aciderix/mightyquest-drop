#!/usr/bin/env python3
"""
validate_codec.py — closed-loop validation of BOTH protocol directions using the
client's REAL serializer/deserializer, under Unicorn. No Windows, no running game.

INCOMING (server->client): a faked parser context feeds our JSON bytes to the
client's real per-field deserialize dispatcher; we read the object back.
OUTGOING (client->server): we fill the object and run the real serialize method,
intercepting the JSON writer primitives to capture the emitted key/value pairs.
A ROUND-TRIP that survives both proves the wire format end-to-end, offline.

The check is contract-driven (see CONTRACTS): each entry carries the deserialize
field-dispatcher, the serialize method, and the field layout recovered from the
decompiled methods. This generalises the proof beyond a single message — here
the boot/login critical path (LoginResult, AccountLite).

Run: python3 re/tools/validate_codec.py
"""
from __future__ import annotations
import struct, sys
sys.path.insert(0, "re/tools")
from emu import Emu, SCRATCH_BASE

EXE = "MightyQuest_unpacked_fixed (1).exe"

# primitive readers/writers (named in 05-SCHEMA-CATALOG.md)
READ_INT, READ_BOOL, READ_STRING = 0x009a8840, 0x009a8c90, 0x009a9450
W_KEY, W_INT, W_STR = 0x009ab550, 0x009aad80, 0x009ab060
# other scalar writer primitives a serialize method may emit (bool/float/datetime
# /uint/...); neutralised so the whole method runs. All are stdcall (ret 4).
W_OTHER = (0x009ab010, 0x009ab3f0, 0x009aae20, 0x009aae70, 0x009aadd0,
           0x009aaf40, 0x009aad30, 0x009aafc0, 0x009aaf50)

CTX, STREAM, SVT = SCRATCH_BASE + 0x1000, SCRATCH_BASE + 0x1300, SCRATCH_BASE + 0x1400
OUT, OBJ, NAME = SCRATCH_BASE + 0x1200, SCRATCH_BASE + 0x2000, SCRATCH_BASE + 0x6000
WRITER, SINK, SINKVT = SCRATCH_BASE + 0x7000, SCRATCH_BASE + 0x7100, SCRATCH_BASE + 0x7200
FAKE_ADVANCE, FAKE_ERROR = SCRATCH_BASE + 0x10, SCRATCH_BASE + 0x20

# field: (json_name, value_offset, kind, capacity_offset_or_None)
CONTRACTS = {
    "LoginResult": {
        "deser": 0x00493440, "ser": 0x0049de80,
        "fields": [("AccountId", 0x04, "int", None),
                   ("ConnectionToken", 0x0c, "str", 0x08),
                   ("ProfileId", 0x2c, "str", 0x28)],
    },
    "AccountLite": {
        "deser": 0x00615db0, "ser": 0x00626c30,
        "fields": [("AccountId", 0x04, "int", None),
                   ("ActivationStatus", 0x08, "int", None),
                   ("DisplayName", 0x10, "str", 0x0c),
                   ("Email", 0x114, "str", 0x110),
                   ("Password", 0x218, "str", 0x214)],
    },
}

# representative test values per field (deterministic)
def testval(kind, i):
    return 1000 + i if kind == "int" else f"val{i}"


def cstr(e, addr, n=40):
    b = e.read(addr, n); z = b.find(b"\x00")
    return b[:z if z >= 0 else n].decode("latin1")


def reader_emu(json_bytes):
    e = Emu(EXE)
    cur = {"i": 1}

    def advance(uc, ecx, a0, a1):
        if cur["i"] < len(json_bytes):
            uc.mem_write(CTX + 4, bytes([json_bytes[cur["i"]]])); cur["i"] += 1
            return 1
        uc.mem_write(CTX + 4, b"\x00"); return 0

    e.write(SVT, b"\x00" * 0x40)
    e.write(SVT + 4, struct.pack("<I", FAKE_ADVANCE))
    e.write(SVT + 0x1c, struct.pack("<I", FAKE_ERROR))
    e.write(STREAM, struct.pack("<I", SVT))
    e.write(CTX, struct.pack("<IBxxxII", STREAM, json_bytes[0], 0, 0))
    e.intercepts = {FAKE_ADVANCE: advance, FAKE_ERROR: (lambda *a: 0)}
    e.intercept_cleanup = {FAKE_ADVANCE: 8}
    return e


def deserialize(spec, values):
    """feed each field's JSON value through the real dispatcher; read the obj."""
    got = {}
    for (name, off, kind, cap), val in zip(spec["fields"], values):
        jb = (str(val).encode() if kind == "int" else b'"' + val.encode() + b'"') + b","
        e = reader_emu(jb)
        e.write(OBJ, b"\x00" * 0x400)
        for _, o2, k2, c2 in spec["fields"]:
            if c2 is not None:
                e.write(OBJ + c2, struct.pack("<I", 0x40))   # string capacity
        e.write(NAME, name.encode() + b"\x00")
        e.call(spec["deser"], [CTX, OBJ, NAME])
        got[name] = (struct.unpack("<i", e.read(OBJ + off, 4))[0] if kind == "int"
                     else cstr(e, OBJ + off))
    return got


def serialize(spec, values):
    """fill the object, run the real serialize, capture emitted key/values."""
    e = Emu(EXE)
    e.write(OBJ, b"\x00" * 0x400)
    for (name, off, kind, cap), val in zip(spec["fields"], values):
        if kind == "int":
            e.write(OBJ + off, struct.pack("<I", val & 0xFFFFFFFF))
        else:
            e.write(OBJ + off, val.encode() + b"\x00")
            if cap is not None:
                e.write(OBJ + cap, struct.pack("<I", 0x40))
    seq, pend = {}, {"k": None}

    def on_key(uc, ecx, a0, a1):
        pend["k"] = cstr(e, a0) or cstr(e, ecx); return 1

    def on_int(uc, ecx, a0, a1):
        p = next((x for x in (a0, a1, ecx) if OBJ <= x < OBJ + 0x400), a1)
        seq[pend["k"]] = struct.unpack("<i", e.read(p, 4))[0]; return 1

    def on_str(uc, ecx, a0, a1):
        p = next((x for x in (a0, a1, ecx) if OBJ <= x < OBJ + 0x400), a0)
        seq[pend["k"]] = cstr(e, p); return 1

    e.intercepts = {W_KEY: on_key, W_INT: on_int, W_STR: on_str}
    for w in W_OTHER:
        e.intercepts[w] = (lambda *a: 1)        # neutralise other writers
    e.intercept_cleanup = {w: 4 for w in (W_KEY, W_INT, W_STR) + W_OTHER}  # stdcall
    e.call(spec["ser"], [WRITER, OBJ])   # WRITER unused (writers intercepted)
    return seq


def validate(name, spec):
    fields = spec["fields"]
    values = [testval(k, i) for i, (_, _, k, _) in enumerate(fields)]
    expect = {f[0]: v for f, v in zip(fields, values)}
    din = deserialize(spec, values)
    sout = serialize(spec, values)
    ok = True
    print(f"\n {name}:")
    for fname in expect:
        i_ok = din.get(fname) == expect[fname]
        o_ok = sout.get(fname) == expect[fname]
        ok &= i_ok and o_ok
        print(f"   {fname:18} in={str(din.get(fname)):8} {'OK' if i_ok else 'X'}  "
              f"out={str(sout.get(fname)):8} {'OK' if o_ok else 'X'}")
    rt = din == sout == expect
    print(f"   round-trip: {'OK' if rt else 'MISMATCH'}")
    return ok and rt


def main():
    print("Closed-loop BOTH-direction validation via the client's REAL codec\n"
          "(in = real deserialize, out = real serialize), offline:")
    results = [validate(n, s) for n, s in CONTRACTS.items()]
    n = len(results)
    print(f"\n[+] {sum(results)}/{n} contracts round-trip cleanly through the client's"
          f" own code, both directions." if all(results)
          else f"\n[!] {n - sum(results)}/{n} contracts mismatched")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
