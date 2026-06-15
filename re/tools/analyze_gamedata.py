#!/usr/bin/env python3
"""
analyze_gamedata.py — mine the real GameplaySettings JSON (the game's own data) to
(1) extract the actual valid enum values per field, (2) catalog the polymorphic
`$type` discriminators, (3) build an observed schema, and (4) cross-validate it
against our reversed schemas (schemas_typed.json).

The raw JSON is Ubisoft game data — NOT committed. Point --data at a local copy;
only the derived catalogs (field names, enum value sets, type list, validation
report) are written under re/catalog/network/gamedata/.

Usage: python3 re/tools/analyze_gamedata.py --data /path/to/GameplaySettings
"""
from __future__ import annotations
import argparse, glob, json, os, re
from collections import Counter, defaultdict

OUT = "re/catalog/network/gamedata"
TPREFIX = "HyperQuest.GameServer.Contracts."
ENUM_VAL = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,48}$")


def kind(v):
    if isinstance(v, bool): return "bool"
    if isinstance(v, int): return "int"
    if isinstance(v, float): return "float"
    if isinstance(v, str): return "string"
    if isinstance(v, list): return "array"
    if isinstance(v, dict): return "object"
    return "null"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="/home/user/gamedata/GameplaySettings")
    args = ap.parse_args()
    files = glob.glob(args.data + "/**/*.JSON", recursive=True) + \
            glob.glob(args.data + "/**/*.json", recursive=True)

    types = Counter()
    fields = defaultdict(lambda: {"kinds": Counter(), "str": Counter()})  # (type,field)
    field_enum = defaultdict(Counter)   # field name -> string values (across types)

    def walk(o):
        if isinstance(o, dict):
            t = o.get("$type", "")
            tn = t.split(",")[0].replace(TPREFIX, "") if t else "?"
            if t:
                types[tn] += 1
            for k, v in o.items():
                if k == "$type":
                    continue
                rec = fields[(tn, k)]
                rec["kinds"][kind(v)] += 1
                if isinstance(v, str):
                    rec["str"][v] += 1
                    field_enum[k][v] += 1
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    parsed = 0
    for f in files:
        try:
            walk(json.load(open(f, encoding="utf-8-sig"))); parsed += 1
        except Exception:
            pass

    os.makedirs(OUT, exist_ok=True)

    # 1) observed $type discriminators
    with open(os.path.join(OUT, "observed_types.txt"), "w") as fh:
        for t, c in types.most_common():
            fh.write(f"{c:7d}  {t}\n")

    # 2) enum value sets — string fields with a bounded set of identifier values
    enums = {}
    for fname, vals in field_enum.items():
        v = [x for x in vals if ENUM_VAL.match(x)]
        if v and len(set(v)) <= 60 and len(v) == len(vals):  # all identifier-like
            enums[fname] = sorted(set(v))
    with open(os.path.join(OUT, "enum_values.json"), "w") as fh:
        json.dump(enums, fh, indent=1, sort_keys=True)

    # 3) observed schema: type -> {field: dominant kind}
    observed = defaultdict(dict)
    for (t, k), rec in fields.items():
        observed[t][k] = rec["kinds"].most_common(1)[0][0]
    with open(os.path.join(OUT, "observed_schema.json"), "w") as fh:
        json.dump(observed, fh, indent=1, sort_keys=True)

    # 4) cross-validate against our reversed schemas
    report = []
    try:
        typed = json.load(open("re/catalog/network/schemas_typed.json"))
    except FileNotFoundError:
        typed = {}
    matched = both_fields = agree = 0
    for c, ov in observed.items():
        if c not in typed:
            continue
        matched += 1
        rev = {f for f, _ in typed[c]["fields"]}
        obs = set(ov)
        common = rev & obs
        both_fields += len(common)
        # field-name agreement (observed fields present in our reversed schema)
        miss = obs - rev
        if miss:
            report.append((c, sorted(miss)))
        agree += len(obs & rev)
    with open(os.path.join(OUT, "validation_report.txt"), "w") as fh:
        fh.write(f"# observed types also in reversed schema: {matched}\n")
        fh.write(f"# observed fields covered by reversed schema: {agree}\n\n")
        fh.write("# observed fields MISSING from our reversed schema (per type):\n")
        for c, miss in sorted(report):
            fh.write(f"{c}: {miss}\n")

    print(f"[+] parsed {parsed}/{len(files)} JSON files")
    print(f"[+] {len(types)} distinct $type contracts -> observed_types.txt")
    print(f"[+] {len(enums)} enum fields with real values -> enum_values.json")
    print(f"[+] observed schema for {len(observed)} types -> observed_schema.json")
    print(f"[+] cross-validation: {matched} types matched our reversed schema, "
          f"{agree} observed fields confirmed; {len(report)} types have extra "
          f"observed fields -> validation_report.txt")


if __name__ == "__main__":
    main()
