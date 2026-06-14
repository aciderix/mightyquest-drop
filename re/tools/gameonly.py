#!/usr/bin/env python3
"""
gameonly.py — Build the "game-only" view at function granularity.

Consumes the Ghidra export (re/catalog/functions.csv) and classifies every
function as GAME (Hyperquest/Zouna), THIRD_PARTY (OpenSSL/curl/zlib/…) or
UNKNOWN, using the source-file hint Ghidra recovered from the build's leftover
assert paths. The basename hint is resolved to a module via the full source
tree (re/catalog/pe/game_source_tree.txt).

Outputs (re/catalog/pe/):
  function_classification.csv   address,size,bucket,module,name
  game_only_summary.txt         function/byte counts per bucket and per module

Run AFTER the Ghidra headless analysis has produced functions.csv:
    python3 re/tools/gameonly.py
"""
from __future__ import annotations
import csv, os, re, sys
from collections import defaultdict

CSV_IN = "re/catalog/functions.csv"
SRC_TREE = "re/catalog/pe/game_source_tree.txt"
OUT_DIR = "re/catalog/pe"

# basename (lowercased) substring -> third-party bucket
THIRD_PARTY_FILES = re.compile(
    r"(eng_|tb_|ssl_|crypto|sha|aes|rsa|bn_|ec_|evp_|x509|pem|asn1"      # openssl
    r"|curl|http_|easy|multi|transfer|url|vtls"                          # libcurl
    r"|inflate|deflate|adler32|crc32|zutil|trees|inftrees"               # zlib
    r"|recast|detour"                                                    # navmesh
    r"|fmod|bink)", re.IGNORECASE)

GAME_DIR = re.compile(r"\\(Hyperquest|Opal\\Zouna)\\", re.IGNORECASE)


def build_basename_index(src_tree_path):
    """basename(lower) -> set of full source paths that share it."""
    idx = defaultdict(set)
    if not os.path.exists(src_tree_path):
        return idx
    with open(src_tree_path, encoding="latin1") as f:
        for line in f:
            p = line.strip()
            if not p:
                continue
            base = re.split(r"[\\/]", p)[-1].lower()
            idx[base].add(p)
    return idx


def module_of(paths):
    for p in paths:
        m = re.search(r"\\(Hyperquest|Opal\\Zouna)\\([A-Za-z0-9_]+)", p, re.IGNORECASE)
        if m:
            return f"{m.group(1)}/{m.group(2)}"
    return None


def classify(hint, basename_idx):
    if not hint:
        return "UNKNOWN", ""
    base = hint.lower()
    paths = basename_idx.get(base, set())
    if any(GAME_DIR.search(p) for p in paths):
        return "GAME", module_of(paths) or "game"
    if THIRD_PARTY_FILES.search(base):
        return "THIRD_PARTY", "third_party"
    if paths:               # known game source file, dir not matched above
        return "GAME", module_of(paths) or "game"
    return "UNKNOWN", ""


def main():
    if not os.path.exists(CSV_IN):
        sys.exit(f"{CSV_IN} not found — run the Ghidra headless analysis first "
                 f"(see re/docs/02-TOOLING.md).")
    basename_idx = build_basename_index(SRC_TREE)

    rows = []
    with open(CSV_IN, newline="") as f:
        for r in csv.DictReader(f):
            bucket, module = classify(r.get("source_hint", ""), basename_idx)
            rows.append((r["address"], int(r["size"]), bucket, module, r["name"]))

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "function_classification.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["address", "size", "bucket", "module", "name"])
        w.writerows(rows)

    by_bucket_n = defaultdict(int); by_bucket_b = defaultdict(int)
    by_module_n = defaultdict(int); by_module_b = defaultdict(int)
    for addr, size, bucket, module, name in rows:
        by_bucket_n[bucket] += 1; by_bucket_b[bucket] += size
        if bucket == "GAME" and module:
            by_module_n[module] += 1; by_module_b[module] += size

    with open(os.path.join(OUT_DIR, "game_only_summary.txt"), "w") as f:
        f.write("# Game-only view (function granularity)\n\n")
        f.write(f"{'bucket':14} {'funcs':>8} {'bytes':>12}\n")
        for b in sorted(by_bucket_n, key=lambda k: -by_bucket_b[k]):
            f.write(f"{b:14} {by_bucket_n[b]:8d} {by_bucket_b[b]:12d}\n")
        f.write("\n# GAME functions by module (labeled subset)\n\n")
        for m in sorted(by_module_n, key=lambda k: -by_module_b[k]):
            f.write(f"  {by_module_n[m]:6d} funcs  {by_module_b[m]:10d} bytes  {m}\n")

    print(f"[+] classified {len(rows)} functions")
    for b in sorted(by_bucket_n, key=lambda k: -by_bucket_b[k]):
        print(f"      {b:12} {by_bucket_n[b]:7d} funcs  {by_bucket_b[b]:11d} bytes")
    print(f"[+] -> {OUT_DIR}/function_classification.csv, game_only_summary.txt")


if __name__ == "__main__":
    main()
