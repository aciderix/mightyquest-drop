#!/usr/bin/env python3
"""gameplay_catalog.py — index + load the FULL decrypted GameplaySettings.

The decrypted catalog (server/catalog/GameplaySettings) is the authoritative
game content: AccountTemplates, Castles, Creatures, Abilities, Buffs, Traps,
Rooms, HeroTemplates, Assignments, ... (27 categories, 8726 JSON files).

Entry naming: "000002 - PVE_00_TUTORIAL_01.JSON" -> id=2, name="PVE_00_TUTORIAL_01".
An entry is either a single .JSON file, or a directory holding the standard
AUDIO/GAMEPLAY/UI/VISUAL.JSON split (merged into {"AUDIO":..,"GAMEPLAY":..,..}).

We take EVERYTHING: nothing is dropped. Lookups by (category, id) or by name.
"""
from __future__ import annotations
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# when packaged as a PyInstaller exe, look for catalog/ next to the executable
_BASE = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else HERE
DEFAULT_ROOT = os.environ.get("MQ_CATALOG", os.path.join(_BASE, "catalog", "GameplaySettings"))
if not os.path.isdir(DEFAULT_ROOT) and os.path.isdir(os.path.join(HERE, "catalog", "GameplaySettings")):
    DEFAULT_ROOT = os.path.join(HERE, "catalog", "GameplaySettings")
_ENTRY_RE = re.compile(r"^(\d+)\s*-\s*(.+?)(?:\.JSON)?$", re.I)


def _load_json(path):
    # decrypted game JSON: utf-8 (sometimes BOM), occasionally tab/space noise
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


class Catalog:
    def __init__(self, root: str = DEFAULT_ROOT):
        self.root = root
        self._index: dict[str, dict[int, tuple[str, str]]] = {}
        self._cache: dict[tuple[str, int], object] = {}
        self._build_index()

    def _build_index(self):
        for cat in sorted(os.listdir(self.root)):
            catdir = os.path.join(self.root, cat)
            if not os.path.isdir(catdir):
                continue
            entries: dict = {}
            for entry in os.listdir(catdir):
                path = os.path.join(catdir, entry)
                m = _ENTRY_RE.match(entry)
                if m:
                    # id-keyed entry: "000002 - PVE_00_TUTORIAL_01[.JSON]"
                    entries[int(m.group(1))] = (m.group(2).strip(), path)
                else:
                    # name-keyed entry (settings/config): "OASIS_EN.JSON" -> "OASIS_EN"
                    key = re.sub(r"\.JSON$", "", entry, flags=re.I).upper()
                    entries[key] = (key, path)
            if entries:
                self._index[cat] = entries

    # ── introspection ────────────────────────────────────────────────────────
    def categories(self):
        return list(self._index)

    def keys(self, cat):
        """All entry keys (int ids and/or str names), ids first then names."""
        ks = list(self._index.get(cat, {}))
        return sorted(k for k in ks if isinstance(k, int)) + \
               sorted(k for k in ks if isinstance(k, str))

    def ids(self, cat):
        return sorted(k for k in self._index.get(cat, {}) if isinstance(k, int))

    def names(self, cat):
        return sorted(k for k in self._index.get(cat, {}) if isinstance(k, str))

    def name(self, cat, eid):
        return self._index[cat][eid][0]

    def has(self, cat, eid):
        return eid in self._index.get(cat, {})

    # ── loading ──────────────────────────────────────────────────────────────
    def get(self, cat, eid):
        """Load one entry. Single file -> its JSON; directory -> merged split."""
        key = (cat, eid)
        if key in self._cache:
            return self._cache[key]
        name, path = self._index[cat][eid]
        if os.path.isdir(path):
            data = {}
            for f in sorted(os.listdir(path)):
                fm = re.match(r"(.+)\.JSON$", f, re.I)
                if fm:
                    data[fm.group(1).upper()] = _load_json(os.path.join(path, f))
        else:
            data = _load_json(path)
        self._cache[key] = data
        return data

    def find(self, cat, name_substr):
        """All ids in a category whose name contains name_substr (case-insensitive)."""
        s = name_substr.lower()
        return sorted(eid for eid, (nm, _) in self._index.get(cat, {}).items()
                      if s in nm.lower())

    def find_one(self, cat, name_substr):
        hits = self.find(cat, name_substr)
        return hits[0] if hits else None


# singleton helper
_CATALOG = None
def catalog() -> Catalog:
    global _CATALOG
    if _CATALOG is None:
        _CATALOG = Catalog()
    return _CATALOG


if __name__ == "__main__":
    import sys, time
    c = Catalog()
    print("=== catalogue GameplaySettings — index ===")
    total = 0
    for cat in c.categories():
        n = len(c.keys(cat))
        total += n
        print(f"  {cat:28} {n:5} entrées")
    print(f"  TOTAL: {total} entrées dans {len(c.categories())} catégories")

    # full-load self-test: prouver qu'on charge TOUT sans erreur
    print("\n=== auto-test: chargement intégral (on prend tout) ===")
    t0 = time.time(); ok = 0; errs = []
    for cat in c.categories():
        for eid in c.keys(cat):
            try:
                c.get(cat, eid); ok += 1
            except Exception as e:
                errs.append(f"{cat}/{eid}: {e}")
    print(f"  chargés OK : {ok}")
    print(f"  erreurs    : {len(errs)}")
    for e in errs[:20]:
        print("    !", e)
    print(f"  durée: {time.time()-t0:.1f}s")
    sys.exit(1 if errs else 0)
