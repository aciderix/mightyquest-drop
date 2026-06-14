#!/usr/bin/env python3
"""
rtti.py — Recover the C++ class catalog from MSVC RTTI in the PE32 image.

The client was built with RTTI enabled, so `.rdata` contains MSVC
TypeDescriptors (`.?AV<class>@@`), Complete Object Locators (COL) and the
vtables that point at them. This recovers:

  - every C++ class/struct name (demangled), categorized by subsystem
  - which classes are actually instantiated (have a vtable) + the vtable VA

Outputs (under --out, default re/catalog/classes/):
  classes_all.txt       every RTTI type name, demangled, sorted
  classes_by_group.txt  grouped by subsystem heuristic (engine _Z, gameplay, …)
  vtables.txt           class -> vtable VA (only classes with a located vtable)

Usage: python3 re/tools/rtti.py ["MightyQuest_unpacked_fixed (1).exe"]
"""
from __future__ import annotations
import argparse, os, re, struct, sys
from collections import Counter, defaultdict

try:
    import pefile
except ImportError:
    sys.exit("pip install pefile")

DEFAULT_EXE = "MightyQuest_unpacked_fixed (1).exe"
TD_RE = re.compile(rb"\.\?A[VUW][^\x00]{1,400}@@")


def demangle_td(name: str) -> str:
    """Best-effort demangle of an MSVC TypeDescriptor name like `.?AVfoo@bar@@`."""
    kind = {"V": "class", "U": "struct", "W": "enum", "T": "union"}.get(name[3], "type")
    body = name[4:]
    if body.endswith("@@"):
        body = body[:-2]
    # Template arguments make the @-segmentation ambiguous; keep them raw.
    if "?$" in body or "@" not in body:
        return f"{kind} {body}"
    segs = body.split("@")
    segs = [s for s in segs if s]
    qualified = "::".join(reversed(segs))  # MSVC stores namespaces innermost-first
    return f"{kind} {qualified}"


def classify(qualified: str) -> str:
    n = qualified.split(" ", 1)[-1]
    if n.endswith("_Z") or "_Z::" in n or "_Z<" in n:
        return "engine (Zouna _Z)"
    if n.startswith("Contracts::") or n.startswith("Contracts."):
        return "network contracts (DTO)"
    if "Controller" in n:
        return "network controllers (RPC)"
    if "Serializer" in n:
        return "network serializers"
    if any(k in n for k in ("Spec", "Settings", "Config")):
        return "gameplay specs/config"
    if any(k in n for k in ("Ability", "Hero", "Castle", "Building", "Attack",
                            "Inventory", "Item", "Loot", "Spell", "Monster",
                            "Trap", "Buff", "Quest", "Objective")):
        return "gameplay"
    if n.startswith("std::") or n.startswith("__") or "::__" in n:
        return "CRT/STL"
    return "other"


def build_va_maps(pe):
    """offset<->VA helpers based on the section table."""
    base = pe.OPTIONAL_HEADER.ImageBase
    secs = []
    for s in pe.sections:
        secs.append((s.PointerToRawData, s.SizeOfRawData,
                     base + s.VirtualAddress, s.Misc_VirtualSize))
    def off_to_va(off):
        for praw, rsz, va, vsz in secs:
            if praw <= off < praw + rsz:
                return va + (off - praw)
        return None
    def va_to_off(va):
        for praw, rsz, secva, vsz in secs:
            if secva <= va < secva + max(rsz, vsz):
                rel = va - secva
                if rel < rsz:
                    return praw + rel
        return None
    return off_to_va, va_to_off


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe", nargs="?", default=DEFAULT_EXE)
    ap.add_argument("--out", default="re/catalog/classes")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    pe = pefile.PE(args.exe, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    with open(args.exe, "rb") as f:
        data = f.read()
    off_to_va, va_to_off = build_va_maps(pe)

    # 1) all type descriptors: map TD-VA -> demangled name
    td_va_to_name = {}
    names = {}
    for m in TD_RE.finditer(data):
        raw = m.group(0).decode("latin1")
        name_off = m.start()
        td_va = off_to_va(name_off - 8)  # TypeDescriptor starts 8 bytes before name
        dem = demangle_td(raw)
        names[raw] = dem
        if td_va is not None:
            td_va_to_name[td_va] = dem

    # 2) Complete Object Locators: a COL has pTypeDescriptor at offset 0x0C.
    #    Scan .rdata for 4-byte VAs equal to a known TD-VA; treat the containing
    #    aligned dword as COL.pTypeDescriptor, then locate the COL and its vtable.
    col_va_to_name = {}
    for s in pe.sections:
        nm = s.Name.rstrip(b"\x00")
        if nm not in (b".rdata", b".data"):
            continue
        blob = data[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
        secva = base + s.VirtualAddress
        for i in range(0, len(blob) - 4, 4):
            ptr = struct.unpack_from("<I", blob, i)[0]
            name = td_va_to_name.get(ptr)
            if name is None:
                continue
            col_va = secva + i - 0x0C  # this dword is COL+0x0C
            col_va_to_name[col_va] = name

    # 3) vtables: a pointer to a COL sits at vtable[-1]; vtable starts at +4.
    vtables = {}
    for s in pe.sections:
        if s.Name.rstrip(b"\x00") not in (b".rdata", b".data"):
            continue
        blob = data[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
        secva = base + s.VirtualAddress
        for i in range(0, len(blob) - 4, 4):
            ptr = struct.unpack_from("<I", blob, i)[0]
            name = col_va_to_name.get(ptr)
            if name is None:
                continue
            vtables[name] = secva + i + 4  # first method slot

    # ---- write catalogs ----
    all_names = sorted(set(names.values()))
    with open(os.path.join(args.out, "classes_all.txt"), "w") as f:
        f.write("\n".join(all_names) + "\n")

    groups = defaultdict(list)
    for dem in all_names:
        groups[classify(dem)].append(dem)
    with open(os.path.join(args.out, "classes_by_group.txt"), "w") as f:
        for g in sorted(groups, key=lambda k: -len(groups[k])):
            f.write(f"## {g}  ({len(groups[g])})\n")
            for n in groups[g]:
                f.write(f"  {n}\n")
            f.write("\n")

    with open(os.path.join(args.out, "vtables.txt"), "w") as f:
        for name in sorted(vtables):
            f.write(f"{vtables[name]:#010x}  {name}\n")

    print(f"[+] {len(all_names)} RTTI type names -> {args.out}/classes_all.txt")
    print(f"[+] {len(vtables)} classes with located vtable -> vtables.txt")
    print("[+] group counts:")
    for g in sorted(groups, key=lambda k: -len(groups[k])):
        print(f"      {len(groups[g]):5d}  {g}")


if __name__ == "__main__":
    main()
