#!/usr/bin/env python3
"""
gen_types.py — turn the recovered schema catalog into neutral type definitions:
JSON Schema (draft-07) and TypeScript interfaces, with precise per-field types.

Inputs:
  re/catalog/network/schemas_typed.json   precise types + direction (preferred)
  re/catalog/network/schemas.json         names-only fallback (wider coverage)
Outputs:
  re/catalog/network/generated/schemas.schema.json
  re/catalog/network/generated/types.ts

Field types: numeric (int/uint/byte/short/ushort/long/ulong/number/double) ->
number; string -> string; datetime -> ISO-8601 string; enum -> a quoted
16-hex-digit string "0x...."; bool -> boolean; array -> T[]; object -> nested T.
obj/arr fields are linked to their child contract by name; plural names are
arrays; a numeric field in a response-only contract whose name matches a contract
is treated as an object (the deserialize side under-detects nested objects).
"""
from __future__ import annotations
import json, os

ND = "re/catalog/network"
OUT = os.path.join(ND, "generated")
NUMERIC = {"int", "uint", "byte", "short", "ushort", "long", "ulong", "number"}

# scalar type -> (json-schema fragment, typescript type)
JS_SCALAR = {
    "double":   ({"type": "number"}, "number"),
    "bool":     ({"type": "boolean"}, "boolean"),
    "string":   ({"type": "string"}, "string"),
    "datetime": ({"type": "string", "format": "date-time"}, "string"),
    "enum":     ({"type": "string", "pattern": "^0x[0-9A-Fa-f]{16}$"}, "string"),
    "unknown":  ({}, "unknown"),
}


def js_scalar(t):
    if t in NUMERIC:
        return {"type": "integer"}, "number"
    return JS_SCALAR.get(t, JS_SCALAR["unknown"])


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

    os.makedirs(OUT, exist_ok=True)

    def js(direction, fname, ftype):
        kind, child = resolve(direction, fname, ftype)
        if kind == "object":
            return {"$ref": f"#/$defs/{child}"} if child else {"type": "object"}
        if kind == "array":
            return {"type": "array", "items": {"$ref": f"#/$defs/{child}"} if child else {}}
        return dict(js_scalar(ftype)[0])

    defs = {}
    for c, v in contracts.items():
        props = {f: js(v["direction"], f, t) for f, t in v["fields"]}
        defs[c] = {"type": "object", "properties": props, "x-direction": v["direction"]}
    with open(os.path.join(OUT, "schemas.schema.json"), "w") as f:
        json.dump({"$schema": "http://json-schema.org/draft-07/schema#",
                   "title": "Mighty Quest server contracts", "$defs": defs},
                  f, indent=1, sort_keys=True)

    def ts(direction, fname, ftype):
        kind, child = resolve(direction, fname, ftype)
        if kind == "object":
            return child or "unknown"
        if kind == "array":
            return (child or "unknown") + "[]"
        return js_scalar(ftype)[1]

    lines = ["// Generated from the reversed schema catalog (re/tools/gen_types.py).",
             "// direction: request = client->server, response = server->client.",
             "// enum fields are wire-encoded as a quoted 16-hex-digit string, e.g.",
             '//   \"0x0000000000000003\"  (not a bare number or a name).', ""]
    for c in sorted(contracts):
        v = contracts[c]
        lines.append(f"/** {v['direction']} */")
        lines.append(f"export interface {c} {{")
        for fname, ftype in v["fields"]:
            tag = f"  // {ftype}" if ftype in ("enum", "datetime") else ""
            lines.append(f"  {fname}: {ts(v['direction'], fname, ftype)};{tag}")
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
