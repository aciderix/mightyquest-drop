#!/usr/bin/env python3
"""
analyze.py — Static recon toolkit for the Mighty Quest for Epic Loot client.

Produces reproducible analysis artifacts from the unpacked PE image:
  - PE layout (sections / entropy / imports / TLS / debug)
  - Categorized strings (game source paths vs third-party libs)
  - Reconstructed game source tree (from assert/debug path strings)
  - Server protocol surface (.NET assembly-qualified contract DTOs)

Usage:
    python3 re/tools/analyze.py [path/to/game.exe] [--out re/artifacts]

Dependencies: pefile (pip install pefile). `strings` falls back to a builtin
ASCII scanner if the system binary is unavailable.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys
from collections import Counter

try:
    import pefile
except ImportError:
    sys.exit("pefile is required: pip install pefile")


DEFAULT_EXE = "MightyQuest_unpacked_fixed (1).exe"

# Source-path roots that belong to the game itself (Ubisoft code).
GAME_ROOTS = {
    "Hyperquest\\Simulation": "Game simulation (core gameplay sim)",
    "Hyperquest\\Gameplay": "Gameplay systems",
    "Hyperquest\\BehaviorTree": "AI / behavior trees",
    "Hyperquest\\GameServerProxies": "Network protocol / server proxies",
    "Hyperquest\\Startup": "Bootstrap / startup",
    "Opal\\Zouna\\Engine": "Zouna engine (Opal)",
    "Opal\\Zouna\\LibPC": "Zouna PC platform layer",
}

# Third-party libraries (NOT the game — strip these from the 'game-only' view).
THIRD_PARTY = {
    "openssl": r"openssl|\\crypto\\|BEGIN (RSA|EC|CERTIFICATE)|SSL routines",
    "libcurl": r"libcurl|curl-|curl\.haxx",
    "zlib": r"\bzlib\b|inflate|deflate 1\.",
    "fmod": r"\bfmod\b|FMOD",
    "bink": r"\bbink\b|RAD Game Tools",
    "recast/detour": r"recast|detour",
    "libcef/chromium": r"libcef|chromium|Chrome/",
    "msvc runtime": r"Visual C\+\+|MSVCR|Microsoft Visual",
    "directx": r"d3dx9|D3DX|Direct3D",
}


def scan_ascii_strings(data: bytes, minlen: int = 6):
    """Yield printable ASCII runs (like `strings -n minlen`)."""
    cur = bytearray()
    for b in data:
        if 0x20 <= b < 0x7F:
            cur.append(b)
        else:
            if len(cur) >= minlen:
                yield cur.decode("ascii")
            cur = bytearray()
    if len(cur) >= minlen:
        yield cur.decode("ascii")


def section_report(pe: pefile.PE) -> str:
    out = ["# PE section layout", ""]
    out.append(f"{'name':10} {'vaddr':>10} {'vsize':>10} {'raw':>10} {'entropy':>8}  note")
    notes = {
        ".text": "code",
        ".rdata": "read-only data / RTTI / vtables",
        ".data": "writable data",
        ".tls": "thread-local storage",
        ".UBX0": "Ubisoft protector artifact (high entropy)",
        ".UBX1": "Ubisoft protector / rebuilt import table (encrypted)",
        ".reloc": "base relocations",
        ".rsrc": "resources (icons/version/manifest)",
    }
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode("latin1")
        out.append(
            f"{name:10} {s.VirtualAddress:#10x} {s.Misc_VirtualSize:#10x} "
            f"{s.SizeOfRawData:#10x} {s.get_entropy():8.3f}  {notes.get(name,'')}"
        )
    out += ["", "# Imported DLLs", ""]
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for e in pe.DIRECTORY_ENTRY_IMPORT:
            dll = e.dll.decode("latin1")
            out.append(f"  {dll}")
    out.append("")
    out.append(f"EntryPoint RVA: {pe.OPTIONAL_HEADER.AddressOfEntryPoint:#x}")
    out.append(f"ImageBase:      {pe.OPTIONAL_HEADER.ImageBase:#x}")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("exe", nargs="?", default=DEFAULT_EXE)
    ap.add_argument("--out", default="re/catalog")
    ap.add_argument("--minlen", type=int, default=6)
    args = ap.parse_args()

    if not os.path.exists(args.exe):
        sys.exit(f"not found: {args.exe}")
    pe_dir = os.path.join(args.out, "pe")
    net_dir = os.path.join(args.out, "network")
    for d in (pe_dir, net_dir):
        os.makedirs(d, exist_ok=True)

    pe = pefile.PE(args.exe, fast_load=True)
    pe.parse_data_directories()
    with open(args.exe, "rb") as f:
        data = f.read()

    # 1) PE layout
    with open(os.path.join(pe_dir, "pe_layout.txt"), "w") as f:
        f.write(section_report(pe))

    # 2) Collect strings once
    strings = list(scan_ascii_strings(data, args.minlen))

    # 3) Reconstruct game source tree
    src_re = re.compile(r"[A-Za-z]:\\HQ\\[^\s\"<>|]*?\.(h|cpp|c|inl|hpp)", re.IGNORECASE)
    src_paths = sorted({m.group(0) for s in strings for m in src_re.finditer(s)})
    with open(os.path.join(pe_dir, "game_source_tree.txt"), "w") as f:
        f.write("\n".join(src_paths) + "\n")

    # 4) Game vs third-party tally
    root_counts: Counter = Counter()
    for p in src_paths:
        for root in GAME_ROOTS:
            if root.lower() in p.lower():
                root_counts[root] += 1
    tp_counts: Counter = Counter()
    blob = "\n".join(strings)
    for name, pat in THIRD_PARTY.items():
        tp_counts[name] = len(re.findall(pat, blob, re.IGNORECASE))

    with open(os.path.join(pe_dir, "module_split.txt"), "w") as f:
        f.write("# GAME modules (Ubisoft source roots) — keep\n\n")
        for root, n in root_counts.most_common():
            f.write(f"  {n:5d}  {root:32}  {GAME_ROOTS[root]}\n")
        f.write("\n# THIRD-PARTY libraries — not the game, strip from game-only view\n\n")
        for name, n in tp_counts.most_common():
            if n:
                f.write(f"  {n:5d}  {name}\n")

    # 5) Server protocol contracts (.NET assembly-qualified type names)
    ctr_re = re.compile(r"[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+,\s*(?:Contracts\.Common|Hyperquest[A-Za-z0-9.]*)")
    contracts = sorted({m.group(0) for s in strings for m in ctr_re.finditer(s)})
    with open(os.path.join(net_dir, "server_contracts.txt"), "w") as f:
        f.write("\n".join(contracts) + "\n")

    # 6) Server RPC controllers (from generated proxy source paths)
    ctl_re = re.compile(r"\\([A-Za-z0-9]+Controller)Base\.cpp", re.IGNORECASE)
    controllers = sorted({m.group(1) for p in src_paths for m in ctl_re.finditer(p)})
    with open(os.path.join(net_dir, "server_controllers.txt"), "w") as f:
        f.write("\n".join(controllers) + "\n")

    print(f"[+] artifacts written under {args.out}/")
    print(f"    pe/pe_layout.txt            PE sections / imports")
    print(f"    pe/game_source_tree.txt     {len(src_paths)} game source files referenced")
    print(f"    pe/module_split.txt         game vs third-party module tally")
    print(f"    network/server_contracts.txt   {len(contracts)} server protocol DTOs")
    print(f"    network/server_controllers.txt {len(controllers)} RPC controllers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
