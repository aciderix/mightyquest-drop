#!/usr/bin/env python3
"""
gen_examples.py — emit an example JSON message for every contract, from the typed
schema catalog, with CONTENT that the client will actually accept:
  number types -> 0 (double -> 0.0); bool -> false; string -> "string";
  datetime -> ISO-8601 string; enum -> "0x0000000000000000" (the client encodes
  enums as a quoted 16-hex-digit value, not a name or a bare number);
  array -> [ <element> ]; object -> nested example.

Input:  re/catalog/network/schemas_typed.json   (precise types + direction)
Output: re/catalog/network/generated/examples.json
"""
from __future__ import annotations
import json, os

ND = "re/catalog/network"
OUT = os.path.join(ND, "generated")
GD = os.path.join(ND, "gamedata")
NUMERIC = {"int", "uint", "byte", "short", "ushort", "long", "ulong", "number"}
SCALAR_VALUE = {"double": 0.0, "bool": False, "string": "string",
                "datetime": "2015-06-15T00:00:00Z", "enum": "0x0000000000000000",
                "unknown": None}

# real enum values + polymorphic $type names, mined from the game's own data
ENUMS = json.load(open(os.path.join(GD, "enum_values.json"))) \
    if os.path.exists(os.path.join(GD, "enum_values.json")) else {}
OBSERVED = set()
_ot = os.path.join(GD, "observed_types.txt")
if os.path.exists(_ot):
    OBSERVED = {ln.split()[-1] for ln in open(_ot) if ln.strip()}
TYPE_NS = "HyperQuest.GameServer.Contracts"   # namespace seen in the game data


def scalar_value(ftype, fname):
    if fname in ENUMS:                 # a real, valid enum member from the data
        return ENUMS[fname][0]
    if ftype in NUMERIC:
        return 0
    return SCALAR_VALUE.get(ftype, None)


def main():
    typed = json.load(open(os.path.join(ND, "schemas_typed.json")))
    known = set(typed)

    def resolve(direction, fname, ftype):
        """(kind, child): 'scalar'|'object'|'array'. Plural names matching a
        singular contract are arrays; response-side numeric matching a contract is
        treated as an object (the deserialize side under-detects nested objects)."""
        plural = fname.endswith("s") and fname[:-1] in known
        child = fname if fname in known else (fname[:-1] if plural else None)
        t = ftype
        if t in NUMERIC and direction == "response" and child:
            t = "object"
        if t == "array":
            return "array", child
        if t == "object":
            return ("array" if plural else "object"), child
        return "scalar", None

    def example(contract, depth, stack):
        if contract not in typed or depth > 4 or contract in stack:
            return {}
        v = typed[contract]
        obj = {}
        # polymorphic discriminator: the client picks the subtype from $type, so
        # nested/contract objects must carry it (every object in the game data does)
        if contract in OBSERVED:
            obj["$type"] = f"{TYPE_NS}.{contract}, {TYPE_NS}"
        for fname, ftype in v["fields"]:
            kind, child = resolve(v["direction"], fname, ftype)
            if kind == "object":
                obj[fname] = example(child, depth + 1, stack | {contract}) if child else {}
            elif kind == "array":
                obj[fname] = [example(child, depth + 1, stack | {contract})] if child else []
            else:
                obj[fname] = scalar_value(ftype, fname)
        return obj

    examples = {c: example(c, 0, frozenset()) for c in typed}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "examples.json"), "w") as f:
        json.dump(examples, f, indent=1, sort_keys=True)
    print(f"[+] {len(examples)} example messages -> {OUT}/examples.json")
    for c in ("LoginResult", "GameServerConnectionConfig"):
        print(f"  {c} = {json.dumps(examples.get(c))}")


if __name__ == "__main__":
    main()
