#!/usr/bin/env python3
"""
gen_types.py — turn the recovered schema catalog into neutral, reusable type
definitions: JSON Schema (draft-07) and TypeScript interfaces.

Inputs:
  re/catalog/network/schemas_typed.json   wire shapes + direction (preferred)
  re/catalog/network/schemas.json         names-only fallback (wider coverage)

Outputs:
  re/catalog/network/generated/schemas.schema.json   one JSON Schema, $defs per contract
  re/catalog/network/generated/types.ts               TS interfaces

Field wire shapes: num (bare number), str (quoted string), bool (true/false),
arr (array), obj (nested object). `arr`/`obj` fields are linked to their child
contract by name when possible. Safety net: a `num` field in a response-only
contract whose name matches a contract is treated as an object — the deserialize
side under-detects nested objects, and there is no serialize side to confirm.
"""
from __future__ import annotations
import json, os

ND = "re/catalog/network"
OUT = os.path.join(ND, "generated")

# wire shape -> (json-schema scalar fragment, typescript scalar type)
SCALAR = {
    "num":  ({"type": "number"}, "number"),
    "str":  ({"type": "string"}, "string"),
    "bool": ({"type": "boolean"}, "boolean"),
    "unknown": ({}, "unknown"),
}


def main():
    typed = json.load(open(os.path.join(ND, "schemas_typed.json")))
    names = json.load(open(os.path.join(ND, "schemas.json")))

    contracts = {}
    for c, v in typed.items():
        contracts[c] = {"direction": v["direction"], "fields": v["fields"]}
    for c, flds in names.items():
        contracts.setdefault(c, {"direction": "unknown",
                                 "fields": [[f, "unknown"] for f in flds]})
    known = set(contracts)

    def resolve(direction, fname, ftype):
        """return (kind, child) where kind is 'scalar'|'object'|'array'.

        - arr shape -> array; obj shape -> object (or array if the name is a
          plural of a known contract, since out-of-band array writers look like
          object writers); num in a response whose name matches a contract ->
          object (deserialize under-detects nested objects)."""
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

    os.makedirs(OUT, exist_ok=True)

    # ---- JSON Schema ----
    def js(direction, fname, ftype):
        kind, child = resolve(direction, fname, ftype)
        if kind == "object":
            return {"$ref": f"#/$defs/{child}"} if child else {"type": "object"}
        if kind == "array":
            return {"type": "array", "items": {"$ref": f"#/$defs/{child}"} if child else {}}
        return dict(SCALAR.get(ftype, SCALAR["unknown"])[0])

    defs = {}
    for c, v in contracts.items():
        props = {f: js(v["direction"], f, t) for f, t in v["fields"]}
        defs[c] = {"type": "object", "properties": props, "x-direction": v["direction"]}
    with open(os.path.join(OUT, "schemas.schema.json"), "w") as f:
        json.dump({"$schema": "http://json-schema.org/draft-07/schema#",
                   "title": "Mighty Quest server contracts", "$defs": defs},
                  f, indent=1, sort_keys=True)

    # ---- TypeScript ----
    def ts(direction, fname, ftype):
        kind, child = resolve(direction, fname, ftype)
        if kind == "object":
            return child or "unknown"
        if kind == "array":
            return (child or "unknown") + "[]"
        return SCALAR.get(ftype, SCALAR["unknown"])[1]

    lines = ["// Generated from the reversed schema catalog (re/tools/gen_types.py).",
             "// direction: request = client->server, response = server->client.",
             "// wire shapes: num->number, str->string, bool->boolean, arr->T[], obj->T.", ""]
    for c in sorted(contracts):
        v = contracts[c]
        lines.append(f"/** {v['direction']} */")
        lines.append(f"export interface {c} {{")
        for fname, ftype in v["fields"]:
            lines.append(f"  {fname}: {ts(v['direction'], fname, ftype)};")
        lines += ["}", ""]
    with open(os.path.join(OUT, "types.ts"), "w") as f:
        f.write("\n".join(lines))

    linked = sum(1 for v in contracts.values() for fn, ft in v["fields"]
                 if resolve(v["direction"], fn, ft)[0] in ("object", "array")
                 and resolve(v["direction"], fn, ft)[1])
    complex_n = sum(1 for v in contracts.values() for fn, ft in v["fields"]
                    if resolve(v["direction"], fn, ft)[0] in ("object", "array"))
    print(f"[+] {len(contracts)} contracts -> JSON Schema + TS")
    print(f"[+] obj/arr fields linked to a child contract: {linked}/{complex_n}")
    print(f"[+] -> {OUT}/schemas.schema.json, {OUT}/types.ts")


if __name__ == "__main__":
    main()
