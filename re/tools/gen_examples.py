#!/usr/bin/env python3
"""
gen_examples.py — emit an example JSON message for every contract, from the typed
schema catalog. Ready-to-serve sample payloads / fixtures for the server stub and
inputs for codec validation.

Input:  re/catalog/network/schemas_typed.json   (wire shapes + direction)
Output: re/catalog/network/generated/examples.json   { contract: <example obj> }
"""
from __future__ import annotations
import json, os

ND = "re/catalog/network"
OUT = os.path.join(ND, "generated")
SCALAR = {"num": 0, "str": "string", "bool": False, "unknown": None}


def main():
    typed = json.load(open(os.path.join(ND, "schemas_typed.json")))
    known = set(typed)

    def link(field):
        if field in known:
            return field
        if field.endswith("s") and field[:-1] in known:
            return field[:-1]
        return None

    def resolve(direction, fname, ftype):
        """(kind, child) — kind is 'scalar'|'object'|'array'. Plural names that
        match a singular contract are arrays; response-side num matching a
        contract is treated as an object (deserialize under-detects objects)."""
        plural = fname.endswith("s") and fname[:-1] in known
        child = fname if fname in known else (fname[:-1] if plural else None)
        s = ftype
        if s == "num" and direction == "response" and child:
            s = "obj"
        if s == "arr":
            return "array", child
        if s == "obj":
            return ("array" if plural else "object"), child
        return "scalar", None

    def example(contract, depth, stack):
        if contract not in typed or depth > 4 or contract in stack:
            return {}
        v = typed[contract]
        obj = {}
        for fname, ftype in v["fields"]:
            kind, child = resolve(v["direction"], fname, ftype)
            if kind == "object":
                obj[fname] = example(child, depth + 1, stack | {contract}) if child else {}
            elif kind == "array":
                obj[fname] = [example(child, depth + 1, stack | {contract})] if child else []
            else:
                obj[fname] = SCALAR.get(ftype, None)
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
