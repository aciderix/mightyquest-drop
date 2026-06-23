#!/usr/bin/env python3
"""Recover authoritative enum name->integer maps from the client's own JS enum
models (GameData/UI/Js/generated/models/*.js: `hyperquest.enums.NAME={K:0,...}`).
These are the integers the client (de)serializes, so they let the server send
enum INTEGERS instead of names (the #1 silent-default bug). Writes
re/catalog/network/gamedata/enum_int_values.json."""
import os, re, json, glob, sys
JSDIR = sys.argv[1] if len(sys.argv) > 1 else "/home/user/port/GameData/Data/UI/Js/generated/models"
OUT = os.path.join(os.path.dirname(__file__), "..", "catalog", "network",
                   "gamedata", "enum_int_values.json")
enums = {}
for fp in glob.glob(os.path.join(JSDIR, "*.js")):
    txt = open(fp, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'hyperquest\.enums\.(\w+)\s*=\s*\{([^}]*)\}', txt):
        mapping = {kv.group(1): int(kv.group(2))
                   for kv in re.finditer(r'(\w+)\s*:\s*(-?\d+)', m.group(2))}
        if mapping:
            enums[m.group(1)] = mapping
json.dump(enums, open(OUT, "w"), indent=1, sort_keys=True)
print("wrote %s (%d enums)" % (OUT, len(enums)))
