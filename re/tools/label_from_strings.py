#!/usr/bin/env python3
"""
label_from_strings.py — Map functions to their origin source file by xref.

The build left assert/log strings carrying full source paths
(`D:\\HQ\\...\\Foo.cpp`) and third-party paths (`.\\crypto\\...\\eng_ctrl.c`,
curl, zlib). Each such string is referenced from the function it belongs to
(pushed as an argument to the assert/log call). By locating every string's
virtual address (VA) inside `.text` and resolving the containing function (from
the Ghidra functions.csv), we recover a function -> source-file map *without*
needing a repaired IAT — and from that, the GAME vs THIRD_PARTY split at
function granularity.

Outputs (re/catalog/pe/):
  function_classification.csv   address,size,bucket,module,source,name
  game_only_summary.txt         function/byte counts per bucket and per module

Usage: python3 re/tools/label_from_strings.py
"""
from __future__ import annotations
import bisect, csv, os, re, struct, sys
from collections import defaultdict

try:
    import pefile
except ImportError:
    sys.exit("pip install pefile")

EXE = "MightyQuest_unpacked_fixed (1).exe"
FUNCS = "re/catalog/functions.csv"
OUT_DIR = "re/catalog/pe"

# Game source paths (Ubisoft build machine) and third-party source paths.
GAME_PATH = re.compile(rb"[A-Za-z]:\\HQ\\[^\x00\"]{4,200}?\.(?:cpp|h|inl|c)", re.I)
TP_PATH = re.compile(rb"(?:\.[\\/])?(?:crypto|openssl|curl|zlib|recast|detour)"
                     rb"[\\/][^\x00\"]{0,200}?\.(?:c|cpp|h)", re.I)

# the real module sits after the ...\Branches\Update3\ prefix
GAME_MODULE = re.compile(r"Update3\\(?:Hyperquest|Opal\\Zouna)\\([A-Za-z0-9_]+)", re.I)
CANON = {m.lower(): m for m in ("Engine", "LibPC", "GameServerProxies", "Gameplay",
                                "Simulation", "BehaviorTree", "Startup", "Hyperquest")}


def basename(p): return re.split(r"[\\/]", p)[-1]


def load_functions(path):
    starts, info = [], {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            a = int(r["address"], 16)
            starts.append(a)
            info[a] = (int(r["size"]), r["name"])
    starts.sort()
    return starts, info


def main():
    if not os.path.exists(FUNCS):
        sys.exit(f"{FUNCS} not found — run the Ghidra headless analysis first.")
    pe = pefile.PE(EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = open(EXE, "rb").read()

    def off_to_va(off):
        for s in pe.sections:
            if s.PointerToRawData <= off < s.PointerToRawData + s.SizeOfRawData:
                return base + s.VirtualAddress + (off - s.PointerToRawData)
        return None

    # 1) collect source-path strings -> {VA: (bucket, module, source)}
    va_info = {}
    for m in GAME_PATH.finditer(data):
        va = off_to_va(m.start())
        if va is None:
            continue
        p = m.group(0).decode("latin1")
        mm = GAME_MODULE.search(p)
        module = CANON.get(mm.group(1).lower(), mm.group(1)) if mm else "Hyperquest"
        va_info[va] = ("GAME", module, basename(p))
    for m in TP_PATH.finditer(data):
        va = off_to_va(m.start())
        if va is None:
            continue
        p = m.group(0).decode("latin1")
        lib = re.search(r"(crypto|openssl|curl|zlib|recast|detour)", p, re.I)
        va_info.setdefault(va, ("THIRD_PARTY", (lib.group(1).lower() if lib else "third_party"),
                                basename(p)))

    # 2) text section bounds
    text = next(s for s in pe.sections if s.Name.rstrip(b"\x00") == b".text")
    tstart, traw, tsize = base + text.VirtualAddress, text.PointerToRawData, text.SizeOfRawData
    tbytes = data[traw:traw + tsize]

    starts, finfo = load_functions(FUNCS)

    # 3) single pass over .text: every 4-byte LE word equal to a known string VA
    #    is an operand referencing that string; attribute it to the containing fn.
    fn_hits = defaultdict(lambda: defaultdict(int))   # fn_addr -> {(bucket,module,src): count}
    vaset = va_info
    for i in range(0, len(tbytes) - 4):
        w = tbytes[i] | (tbytes[i+1] << 8) | (tbytes[i+2] << 16) | (tbytes[i+3] << 24)
        meta = vaset.get(w)
        if meta is None:
            continue
        insn_va = tstart + i
        idx = bisect.bisect_right(starts, insn_va) - 1
        if idx < 0:
            continue
        fa = starts[idx]
        size, _ = finfo[fa]
        if insn_va >= fa + size + 16:   # not within this function's body
            continue
        fn_hits[fa][meta] += 1

    # 4) decide a bucket/module/source per labeled function (most-referenced wins)
    classification = {}
    for fa, metas in fn_hits.items():
        (bucket, module, src), _ = max(metas.items(), key=lambda kv: kv[1])
        classification[fa] = (bucket, module, src)

    # 5) write full classification (labeled + unknown)
    os.makedirs(OUT_DIR, exist_ok=True)
    by_bucket_n = defaultdict(int); by_bucket_b = defaultdict(int)
    by_module_n = defaultdict(int); by_module_b = defaultdict(int)
    with open(os.path.join(OUT_DIR, "function_classification.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["address", "size", "bucket", "module", "source", "name"])
        for fa in starts:
            size, name = finfo[fa]
            bucket, module, src = classification.get(fa, ("UNKNOWN", "", ""))
            w.writerow([f"0x{fa:08x}", size, bucket, module, src, name])
            by_bucket_n[bucket] += 1; by_bucket_b[bucket] += size
            if bucket == "GAME":
                by_module_n[module] += 1; by_module_b[module] += size

    with open(os.path.join(OUT_DIR, "game_only_summary.txt"), "w") as f:
        f.write("# Game-only view (function granularity, via source-path xref)\n\n")
        f.write(f"{'bucket':14}{'funcs':>9}{'bytes':>12}\n")
        for b in sorted(by_bucket_n, key=lambda k: -by_bucket_b[k]):
            f.write(f"{b:14}{by_bucket_n[b]:9d}{by_bucket_b[b]:12d}\n")
        f.write("\n# GAME functions by module (labeled subset)\n\n")
        for m in sorted(by_module_n, key=lambda k: -by_module_b[k]):
            f.write(f"  {by_module_n[m]:6d} funcs  {by_module_b[m]:10d} bytes  {m}\n")

    labeled = len(classification)
    print(f"[+] {labeled} functions labeled from source-path xrefs "
          f"({labeled*100//len(starts)}% of {len(starts)})")
    for b in sorted(by_bucket_n, key=lambda k: -by_bucket_b[k]):
        print(f"      {b:12}{by_bucket_n[b]:8d} funcs {by_bucket_b[b]:11d} bytes")
    print(f"[+] -> {OUT_DIR}/function_classification.csv, game_only_summary.txt")


if __name__ == "__main__":
    main()
