#!/usr/bin/env python3
"""
subsystems.py — Split the reconstructed game source tree into per-subsystem
file lists, giving a bird's-eye map of every game system (combat, AI, loot,
castle, objectives, …).

Reads  re/catalog/pe/game_source_tree.txt
Writes re/catalog/subsystems/<module>_files.txt  (deduped, path after Update3\)
       re/catalog/subsystems/index.txt           (file counts per module)

Usage: python3 re/tools/subsystems.py
"""
from __future__ import annotations
import os, re, sys
from collections import defaultdict

SRC = "re/catalog/pe/game_source_tree.txt"
OUT = "re/catalog/subsystems"

# canonical module key from a full source path
MOD = re.compile(r"Update3\\(?:Hyperquest|Opal)\\(?:Zouna\\)?([A-Za-z0-9_]+)", re.I)
CANON = {m.lower(): m for m in ("Simulation", "Gameplay", "Engine", "LibPC",
                                "BehaviorTree", "GameServerProxies", "Startup")}


def rel(p):
    m = re.search(r"Update3\\(.+)", p, re.I)
    return (m.group(1) if m else p).replace("/", "\\")


def main():
    if not os.path.exists(SRC):
        sys.exit(f"{SRC} not found — run analyze.py first.")
    os.makedirs(OUT, exist_ok=True)
    mods = defaultdict(set)
    for line in open(SRC, encoding="latin1"):
        p = line.strip()
        if not p:
            continue
        m = MOD.search(p)
        key = CANON.get(m.group(1).lower(), m.group(1)) if m else "Other"
        mods[key].add(rel(p))

    index = []
    for key in sorted(mods, key=lambda k: -len(mods[k])):
        files = sorted(mods[key])
        with open(os.path.join(OUT, f"{key}_files.txt"), "w") as f:
            f.write("\n".join(files) + "\n")
        index.append((key, len(files)))

    with open(os.path.join(OUT, "index.txt"), "w") as f:
        f.write("# Game subsystems by referenced-source-file count\n\n")
        for key, n in index:
            f.write(f"  {n:5d}  {key}\n")

    print("[+] subsystem catalogs written to", OUT)
    for key, n in index:
        print(f"      {n:5d}  {key}")


if __name__ == "__main__":
    main()
