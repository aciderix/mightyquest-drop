#!/usr/bin/env python3
"""
gen_examples.py — emit an example JSON message for every contract, from the
typed schema catalog. These are ready-to-serve sample payloads / test fixtures
for the community-server stub (and inputs for codec validation via Unicorn).

Input:  re/catalog/network/schemas_typed.json
Output: re/catalog/network/generated/examples.json   { contract: <example obj> }
"""
from __future__ import annotations
import json, os

ND = "re/catalog/network"
OUT = os.path.join(ND, "generated")
SAMPLE = {
    "int": 0, "number": 0, "float": 0.0, "string": "string",
    "bool": False, "datetime": "2015-01-01T00:00:00Z", "duration": "0",
    "unknown": None,
}


def main():
    typed = json.load(open(os.path.join(ND, "schemas_typed.json")))
    known = set(typed)

    def link(field):
        if field in known:
            return field
        if field.endswith("s") and field[:-1] in known:
            return field[:-1]
        return None

    def example(contract, depth, stack):
        if contract not in typed or depth > 4 or contract in stack:
            return {}
        obj = {}
        for fname, ftype in typed[contract]["fields"]:
            if ftype == "object":
                child = link(fname)
                obj[fname] = (example(child, depth + 1, stack | {contract})
                              if child else {})
            else:
                obj[fname] = SAMPLE.get(ftype, None)
        return obj

    examples = {c: example(c, 0, frozenset()) for c in typed}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "examples.json"), "w") as f:
        json.dump(examples, f, indent=1, sort_keys=True)
    print(f"[+] {len(examples)} example messages -> {OUT}/examples.json")
    for c in ("LoginResult", "GameServerConnectionConfig"):
        print(f"\n  {c} = {json.dumps(examples.get(c))}")


if __name__ == "__main__":
    main()
