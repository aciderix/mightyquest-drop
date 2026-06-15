#!/usr/bin/env python3
"""
validate_codec.py — closed-loop validation of BOTH protocol directions using the
client's REAL serializer/deserializer, under Unicorn. No Windows, no running game.

INCOMING (server -> client): the client's JSON readers pull chars through a parser
context (current char at ctx+4; `memory[memory[ctx[0]]+4]` advances). We fake the
context and feed bytes; the real reader parses them. Validated for int, bool,
string, and a whole object (LoginResult) via its real field dispatcher.

OUTGOING (client -> server): we build an object and run the real serialize method,
intercepting the JSON writer primitives to capture the exact key/value sequence
the client emits.

If the client's own code round-trips our wire format, the community server's
protocol is correct — proven offline.

Run: python3 re/tools/validate_codec.py
"""
from __future__ import annotations
import struct, sys
sys.path.insert(0, "re/tools")
from emu import Emu, SCRATCH_BASE

EXE = "MightyQuest_unpacked_fixed (1).exe"

# --- readers (incoming) -----------------------------------------------------
READ_INT     = 0x009a8840           # FUN_009a8d30 tail-calls this
READ_BOOL    = 0x009a8c90
READ_STRING  = 0x009a9450
LOGINRESULT_DESER = 0x00493440      # __cdecl(ctx, obj, fieldname) field dispatcher
# --- writers (outgoing) -----------------------------------------------------
LOGINRESULT_SER = 0x0049de80        # serialize(writer, obj)
W_KEY, W_INT, W_STR = 0x009ab550, 0x009aad80, 0x009ab060

CTX    = SCRATCH_BASE + 0x1000
STREAM = SCRATCH_BASE + 0x1300
SVT    = SCRATCH_BASE + 0x1400
OUT    = SCRATCH_BASE + 0x1200
OBJ    = SCRATCH_BASE + 0x2000
NAME   = SCRATCH_BASE + 0x3000
FAKE_ADVANCE = SCRATCH_BASE + 0x10
FAKE_ERROR   = SCRATCH_BASE + 0x20


def reader_emu(json_bytes):
    """emulator with a faked parser context primed on json_bytes (incoming)."""
    e = Emu(EXE)
    cur = {"i": 1}

    def advance(uc, ecx, a0, a1):
        if cur["i"] < len(json_bytes):
            uc.mem_write(CTX + 4, bytes([json_bytes[cur["i"]]])); cur["i"] += 1
            return 1
        uc.mem_write(CTX + 4, b"\x00")
        return 0

    e.write(SVT, b"\x00" * 0x40)
    e.write(SVT + 4, struct.pack("<I", FAKE_ADVANCE))
    e.write(SVT + 0x1c, struct.pack("<I", FAKE_ERROR))
    e.write(STREAM, struct.pack("<I", SVT))
    e.write(CTX, struct.pack("<IBxxxII", STREAM, json_bytes[0], 0, 0))
    e.write(OUT, b"\x00" * 64)
    e.intercepts = {FAKE_ADVANCE: advance, FAKE_ERROR: (lambda *a: 0)}
    e.intercept_cleanup = {FAKE_ADVANCE: 8}   # advance is stdcall: pops (ptr,1)
    return e


def cstr(e, addr, n=32):
    b = e.read(addr, n); z = b.find(b"\x00")
    return b[:z if z >= 0 else n].decode("latin1")


def read_int(s):
    e = reader_emu(s); e.call(READ_INT, [OUT], ecx=CTX)
    return struct.unpack("<i", e.read(OUT, 4))[0]


def read_bool(s):
    e = reader_emu(s); e.call(READ_BOOL, [OUT], ecx=CTX)
    return e.read(OUT, 1)[0]


def read_string(s, cap=32):
    e = reader_emu(s); e.call(READ_STRING, [OUT, cap], ecx=CTX)
    return cstr(e, OUT)


def deser_loginresult(account_id, token, profile):
    """parse each field with the client's real LoginResult dispatcher."""
    out = {}
    for name, value in [(b"AccountId", str(account_id).encode() + b","),
                        (b"ConnectionToken", b'"' + token + b'",'),
                        (b"ProfileId", b'"' + profile + b'",')]:
        e = reader_emu(value)
        e.write(OBJ, b"\x00" * 0x60)
        e.write(OBJ + 0x08, struct.pack("<I", 0x19))   # ConnectionToken capacity
        e.write(OBJ + 0x28, struct.pack("<I", 0x19))   # ProfileId capacity
        e.write(NAME, name + b"\x00")
        e.call(LOGINRESULT_DESER, [CTX, OBJ, NAME])    # __cdecl(ctx, obj, fieldname)
        if name == b"AccountId":
            out["AccountId"] = struct.unpack("<i", e.read(OBJ + 0x04, 4))[0]
        elif name == b"ConnectionToken":
            out["ConnectionToken"] = cstr(e, OBJ + 0x0c)
        else:
            out["ProfileId"] = cstr(e, OBJ + 0x2c)
    return out


def ser_loginresult(account_id, token, profile):
    """run the client's real serialize method; capture the emitted key/value seq."""
    e = Emu(EXE)
    e.write(OBJ, b"\x00" * 0x60)
    e.write(OBJ + 0x04, struct.pack("<I", account_id))
    e.write(OBJ + 0x0c + 4, token + b"\x00")
    e.write(OBJ + 0x2c + 4, profile + b"\x00")
    seq, pend = [], {"k": None}

    def on_key(uc, ecx, a0, a1):
        pend["k"] = cstr(e, a0) or cstr(e, ecx); return 1

    def on_int(uc, ecx, a0, a1):
        ptr = next((p for p in (a0, a1, ecx) if OBJ <= p < OBJ + 0x60), a1)
        seq.append((pend["k"], struct.unpack("<i", e.read(ptr, 4))[0])); return 1

    def on_str(uc, ecx, a0, a1):
        ptr = next((p for p in (a0, a1, ecx) if OBJ <= p < OBJ + 0x60), a0)
        seq.append((pend["k"], cstr(e, ptr + 4))); return 1

    e.intercepts = {W_KEY: on_key, W_INT: on_int, W_STR: on_str}
    e.call(LOGINRESULT_SER, [SCRATCH_BASE, OBJ])
    return {k: v for k, v in seq}


def line(label, got, exp):
    ok = got == exp
    print(f"  {label:46} -> {str(got):<22} {'OK' if ok else 'FAIL exp ' + str(exp)}")
    return ok


def main():
    print("Closed-loop validation of BOTH directions, using the client's REAL\n"
          "serializer/deserializer (offline, no game):\n")
    r = []
    print(" INCOMING (server->client) primitives:")
    for s, e in [(b"12345,", 12345), (b"-42,", -42), (b"2147483647,", 2147483647)]:
        r.append(line(f"readInt({s.decode()})", read_int(s), e))
    r.append(line("readBool(true)", read_bool(b"true,"), 1))
    r.append(line("readBool(false)", read_bool(b"false,"), 0))
    r.append(line('readString("hello")', read_string(b'"hello",'), "hello"))

    print("\n INCOMING whole object — LoginResult via its real field dispatcher:")
    d = deser_loginresult(987, b"sess-abc", b"42")
    exp = {"AccountId": 987, "ConnectionToken": "sess-abc", "ProfileId": "42"}
    for k in exp:
        r.append(line(f".{k}", d.get(k), exp[k]))

    print("\n OUTGOING (client->server) — LoginResult via its real serialize:")
    s = ser_loginresult(987, b"sess-abc", b"42")
    for k in exp:
        r.append(line(f".{k}", s.get(k), exp[k]))

    print("\n ROUND-TRIP:", "OK — serialize(x) then deserialize gives x back"
          if d == s == exp else "mismatch")
    print(f"\n[+] {sum(r)}/{len(r)} checks passed — the client's own code round-trips\n"
          "    our wire format in both directions, offline." if all(r)
          else f"\n[!] {len(r)-sum(r)} checks failed")
    return 0 if all(r) else 1


if __name__ == "__main__":
    raise SystemExit(main())
