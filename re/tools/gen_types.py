#!/usr/bin/env python3
"""
gen_types.py — turn the recovered schema catalog into neutral, reusable type
definitions: JSON Schema (draft-07) and TypeScript interfaces.

Inputs:
  re/catalog/network/schemas_typed.json   typed fields + direction (preferred)
  re/catalog/network/schemas.json         names-only fallback (wider coverage)

Outputs:
  re/catalog/network/generated/schemas.schema.json   one JSON Schema, $defs per contract
  re/catalog/network/generated/types.ts               TS interfaces

`object` fields are linked to a child contract when a contract of the same name
exists (e.g. field `CastleLoadConfig` -> type `CastleLoadConfig`); otherwise they
fall back to a generic object / `unknown`.
"""
from __future__ import annotations
import json, os, re

ND = "re/catalog/network"
OUT = os.path.join(ND, "generated")

# our recovered type -> (json-schema fragment builder, typescript type)
JS = {
    "int":      ({"type": "integer"}, "number"),
    "number":   ({"type": "number"}, "number"),
    "float":    ({"type": "number"}, "number"),
    "string":   ({"type": "string"}, "string"),
    "bool":     ({"type": "boolean"}, "boolean"),
    "datetime": ({"type": "string", "format": "date-time"}, "string"),
    "duration": ({"type": "string"}, "string"),
    "unknown":  ({}, "unknown"),
}


def main():
    typed = json.load(open(os.path.join(ND, "schemas_typed.json")))
    names = json.load(open(os.path.join(ND, "schemas.json")))

    # unified contract -> [(field, type, direction)]
    contracts = {}
    for c, v in typed.items():
        contracts[c] = {"direction": v["direction"], "fields": v["fields"]}
    for c, flds in names.items():
        contracts.setdefault(c, {"direction": "unknown",
                                 "fields": [[f, "unknown"] for f in flds]})

    known = set(contracts)

    def link_object(field_name):
        """resolve an `object` field to a child contract by name, else generic."""
        if field_name in known:
            return field_name
        # array-ish heuristic: trailing 's' plural -> singular contract
        if field_name.endswith("s") and field_name[:-1] in known:
            return field_name[:-1]
        return None

    os.makedirs(OUT, exist_ok=True)

    # ---- JSON Schema ----
    defs = {}
    for c, v in contracts.items():
        props = {}
        for fname, ftype in v["fields"]:
            if ftype == "object":
                ref = link_object(fname)
                props[fname] = ({"$ref": f"#/$defs/{ref}"} if ref
                                else {"type": "object"})
            else:
                props[fname] = dict(JS.get(ftype, JS["unknown"])[0])
        defs[c] = {"type": "object", "properties": props,
                   "x-direction": v["direction"]}
    schema = {"$schema": "http://json-schema.org/draft-07/schema#",
              "title": "Mighty Quest server contracts", "$defs": defs}
    with open(os.path.join(OUT, "schemas.schema.json"), "w") as f:
        json.dump(schema, f, indent=1, sort_keys=True)

    # ---- TypeScript ----
    def ts_type(fname, ftype):
        if ftype == "object":
            ref = link_object(fname)
            return ref if ref else "unknown"
        return JS.get(ftype, JS["unknown"])[1]

    lines = ["// Generated from the reversed schema catalog (re/tools/gen_types.py).",
             "// direction: request = client->server, response = server->client.", ""]
    for c in sorted(contracts):
        v = contracts[c]
        lines.append(f"/** {v['direction']} */")
        lines.append(f"export interface {c} {{")
        for fname, ftype in v["fields"]:
            lines.append(f"  {fname}: {ts_type(fname, ftype)};")
        lines.append("}")
        lines.append("")
    with open(os.path.join(OUT, "types.ts"), "w") as f:
        f.write("\n".join(lines))

    nlinked = sum(1 for v in contracts.values() for fn, ft in v["fields"]
                  if ft == "object" and link_object(fn))
    nobj = sum(1 for v in contracts.values() for _, ft in v["fields"] if ft == "object")
    print(f"[+] {len(contracts)} contracts -> JSON Schema + TS")
    print(f"[+] object fields linked to a child contract: {nlinked}/{nobj}")
    print(f"[+] -> {OUT}/schemas.schema.json, {OUT}/types.ts")


if __name__ == "__main__":
    main()
