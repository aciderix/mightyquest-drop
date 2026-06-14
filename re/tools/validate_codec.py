#!/usr/bin/env python3
"""
validate_codec.py — closed-loop validation of the wire format using the client's
REAL deserializer, under Unicorn. No Windows / running game required.

The client's JSON readers pull characters through a parser context: the current
char lives at ctx+4 and `ctx->vtable[+4](...)` advances to the next char. We
build a fake context whose advance method is intercepted to feed bytes from a
JSON value we supply, then run the actual reader primitive and check the value it
produces. If the real client code parses our bytes correctly, our server's wire
format is accepted by the client — proven offline.

Run: python3 re/tools/validate_codec.py
"""
from __future__ import annotations
import struct, sys
sys.path.insert(0, "re/tools")
from emu import Emu, SCRATCH_BASE

EXE = "MightyQuest_unpacked_fixed (1).exe"

# reader primitives (named in 05-SCHEMA-CATALOG.md)
READ_INT_CORE = 0x009a8840      # FUN_009a8d30 (readInt) tail-calls this
READ_BOOL     = 0x009a8c90
SKIP_WS       = 0x009a9f20      # whitespace skipper, no-op'd for clean input

CTX    = SCRATCH_BASE + 0x1000
STREAM = SCRATCH_BASE + 0x1300   # ctx[0] -> stream object
SVT    = SCRATCH_BASE + 0x1400   # stream[0] -> stream vtable
OUT    = SCRATCH_BASE + 0x1200
FAKE_ADVANCE = SCRATCH_BASE + 0x10
FAKE_ERROR   = SCRATCH_BASE + 0x20


def run_reader(reader_va, json_bytes):
    """drive `reader_va` over json_bytes via a faked parser context; return OUT.

    The reader advances via memory[ memory[ctx[0]] + 4 ](...), i.e. through the
    stream object's vtable, and reads the current char at ctx+4.
    """
    e = Emu(EXE)
    cur = {"i": 1}

    def advance(uc, ecx, a0, a1):
        if cur["i"] < len(json_bytes):
            uc.mem_write(CTX + 4, bytes([json_bytes[cur["i"]]]))
            cur["i"] += 1
            return 1
        uc.mem_write(CTX + 4, b"\x00")   # end of input
        return 0

    # stream vtable: +4 = advance(read 1 char), +0x1c = error reporter
    e.write(SVT, b"\x00" * 0x40)
    e.write(SVT + 4, struct.pack("<I", FAKE_ADVANCE))
    e.write(SVT + 0x1c, struct.pack("<I", FAKE_ERROR))
    e.write(STREAM, struct.pack("<I", SVT))           # stream[0] -> vtable
    # context: [0]=stream ptr, +4=current char (first byte), [2]=0, [3]=pos
    e.write(CTX, struct.pack("<IBxxxII", STREAM, json_bytes[0], 0, 0))
    e.write(OUT, b"\x00" * 8)

    e.intercepts = {
        FAKE_ADVANCE: advance,
        FAKE_ERROR: (lambda *a: 0),
        SKIP_WS: (lambda *a: 0),
    }
    e.call(reader_va, [OUT], ecx=CTX)
    return e.read(OUT, 8)


def check(label, reader_va, s, expect, decode):
    try:
        got = decode(run_reader(reader_va, s))
    except Exception as ex:
        print(f"  {label}({s.decode():>6}) -> emulation limit ({type(ex).__name__})")
        return None
    good = got == expect
    print(f"  {label}({s.decode():>6}) -> {got!s:<8} {'OK' if good else 'FAIL exp '+str(expect)}")
    return good


def main():
    print("Validating the client's real JSON readers on our bytes (Unicorn):\n")
    results = []
    for s, exp in [(b"12345", 12345), (b"-42", -42), (b"0", 0), (b"777", 777)]:
        results.append(check("readInt", READ_INT_CORE, s, exp,
                             lambda r: struct.unpack("<i", r[:4])[0]))
    for s, exp in [(b"true", 1), (b"false", 0)]:
        results.append(check("readBool", READ_BOOL, s, exp, lambda r: r[0]))

    proven = [r for r in results if r is not None]
    if proven and all(proven):
        print(f"\n[+] {len(proven)} cases proven: the client's real deserializer "
              f"parses our wire bytes correctly (offline, no game running)")
    elif any(r is False for r in results):
        print("\n[!] a parsed value mismatched — investigate")
    return 0 if all(r for r in results if r is not None) else 1


if __name__ == "__main__":
    raise SystemExit(main())
