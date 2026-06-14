#!/usr/bin/env python3
"""
demo_loginresult.py — End-to-end proof: emulate LoginResult::Serialize under
Unicorn and capture the (key, value) sequence it emits, confirming the JSON
schema recovered statically in re/docs/04-WIRE-FORMAT-LOGIN.md.

We build a LoginResult object in emulated memory (field layout taken from the
copy-constructor at FUN_00468770) and run the serialize method FUN_0049de80,
intercepting the three JSON-writer primitives so we observe what it writes
without needing a real output stream.
"""
import struct, sys
sys.path.insert(0, "re/tools")
from emu import Emu, SCRATCH_BASE

EXE = "MightyQuest_unpacked_fixed (1).exe"
SERIALIZE = 0x0049de80          # LoginResult serialize method (vtable slot 3)
WRITE_KEY = 0x009ab550          # writeKey(name)
WRITE_INT = 0x009aad80          # writeInt(&int)
WRITE_STR = 0x009ab060          # writeString(&String_Z)


def cstr(e, addr, n=64):
    if not addr:
        return None
    b = e.read(addr, n)
    z = b.find(b"\x00")
    s = b[: z if z >= 0 else n]
    return s.decode("latin1") if all(32 <= c < 127 for c in s) and s else None


def main():
    e = Emu(EXE)
    obj = SCRATCH_BASE + 0x400
    # field layout (from the copy-ctor): +4 int, +0xc String, +0x2c String
    e.write(obj + 4, struct.pack("<I", 12345))                 # AccountId
    e.write(obj + 0xc + 4, b"TESTTOKEN\x00")                   # ConnectionToken inline buf
    e.write(obj + 0x2c + 4, b"PROFILE42\x00")                  # ProfileId inline buf

    e.intercepts = {WRITE_KEY: "key", WRITE_INT: "int", WRITE_STR: "str"}
    e.call(SERIALIZE, [SCRATCH_BASE, obj])                     # (writer, object)

    def into_obj(*cands):
        """pick the argument that points inside our object."""
        for c in cands:
            if obj <= c < obj + 0x100:
                return c
        return cands[0]

    print("Captured serialization sequence (dynamic, via Unicorn):\n")
    fields = []
    pending_key = None
    for label, ecx, edx, a0, a1 in e.trace_calls:
        if label == "key":
            pending_key = cstr(e, a0) or cstr(e, ecx)
        elif label == "int":
            ptr = into_obj(a0, a1, ecx, edx)
            val = struct.unpack("<I", e.read(ptr, 4))[0]
            fields.append((pending_key, val)); pending_key = None
        elif label == "str":
            ptr = into_obj(a0, a1, ecx, edx) + 4   # inline buf after capacity dword
            fields.append((pending_key, cstr(e, ptr))); pending_key = None

    for k, v in fields:
        print(f'   "{k}": {v!r}')
    print("\n[+] matches static schema: AccountId(int), ConnectionToken(str), ProfileId(str)"
          if [k for k, _ in fields] == ["AccountId", "ConnectionToken", "ProfileId"]
          else "\n[!] sequence differs from static schema — investigate")


if __name__ == "__main__":
    main()
