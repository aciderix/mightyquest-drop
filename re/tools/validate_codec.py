#!/usr/bin/env python3
"""
validate_codec.py — closed-loop validation of the wire format using the client's
REAL deserializer, under Unicorn. No Windows / running game required.

Concept: the client's JSON readers pull characters through a parser context — the
current char sits at ctx+4 and `memory[memory[ctx[0]]+4](...)` (the stream
vtable's advance slot) loads the next char. We build a fake context whose advance
method is intercepted to feed bytes from JSON we supply, run the actual reader,
and check the value produced. If the real client code parses our bytes, our
server's wire format is accepted by the client — proven offline.

Status: the integer reader is validated end-to-end. bool/string/whole-object
readers route through the codec's error/append helpers whose nested calling
conventions need more harness work (callee stack cleanup) — tracked as WIP.

Run: python3 re/tools/validate_codec.py
"""
from __future__ import annotations
import struct, sys
sys.path.insert(0, "re/tools")
from emu import Emu, SCRATCH_BASE

EXE = "MightyQuest_unpacked_fixed (1).exe"
READ_INT_CORE = 0x009a8840          # FUN_009a8d30 (readInt) tail-calls this

CTX    = SCRATCH_BASE + 0x1000
STREAM = SCRATCH_BASE + 0x1300      # ctx[0] -> stream object
SVT    = SCRATCH_BASE + 0x1400      # stream[0] -> stream vtable
OUT    = SCRATCH_BASE + 0x1200
FAKE_ADVANCE = SCRATCH_BASE + 0x10
FAKE_ERROR   = SCRATCH_BASE + 0x20


def new_emu(json_bytes):
    """fresh emulator with a faked parser context primed on json_bytes[0]."""
    e = Emu(EXE)
    cur = {"i": 1}

    def advance(uc, ecx, a0, a1):
        if cur["i"] < len(json_bytes):
            uc.mem_write(CTX + 4, bytes([json_bytes[cur["i"]]]))
            cur["i"] += 1
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
    return e


def read_int(s):
    e = new_emu(s)
    e.call(READ_INT_CORE, [OUT], ecx=CTX)
    return struct.unpack("<i", e.read(OUT, 4))[0]


def main():
    print("Closed-loop codec validation — running the client's REAL integer\n"
          "reader on bytes we supply (no game, no Windows):\n")
    ok = True
    for s, exp in [(b"12345,", 12345), (b"-42,", -42), (b"0,", 0),
                   (b"777,", 777), (b"2147483647,", 2147483647)]:
        got = read_int(s)
        good = got == exp
        ok &= good
        print(f"  readInt({s.decode():>12}) -> {got:<12} {'OK' if good else 'FAIL exp '+str(exp)}")

    print("\n[+] proven: the client's real deserializer parses our integer wire "
          "bytes correctly, offline." if ok else "\n[!] mismatch — investigate")
    print("[i] bool/string/whole-object readers: harness WIP (their error/append "
          "helpers need callee-cleanup handling in the intercept layer).")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
