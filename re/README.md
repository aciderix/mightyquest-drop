# `re/` — Mighty Quest reverse-engineering workspace

Static-analysis tooling and findings for the unpacked client
`MightyQuest_unpacked_fixed (1).exe` (repo root). Goal: understand the game
(Zouna engine + Hyperquest gameplay) well enough to stand up a **community
server** for this abandoned online action-RPG.

```
re/
├── tools/        reproducible analysis scripts
│   └── analyze.py    PE layout, module split, source tree, server contracts
├── artifacts/    generated output (regenerate any time, see below)
│   ├── pe_layout.txt
│   ├── module_split.txt         game vs third-party
│   ├── game_source_tree.txt     ~4800 referenced source files
│   ├── server_controllers.txt   30 RPC controllers (the server API)
│   └── server_contracts.txt     100+ .NET DTOs (the wire types)
└── docs/
    ├── 00-ARCHITECTURE.md   tech stack, engine, module map
    ├── 01-SERVER-API.md     the 30 controllers + protocol notes
    └── ROADMAP.md           phased plan to a playable community server
```

## Reproduce

```bash
pip install pefile capstone
python3 re/tools/analyze.py            # uses the .exe at repo root
```

## TL;DR of findings
- Engine: **Zouna** (Ubisoft, codename Opal). D3D9 renderer, **CEF/HTML UI**,
  FMOD audio, Bink video, Recast navmesh.
- The client embeds the **full server contract**: 30 RPC controllers + 100+ DTOs.
- Reviving the game = **reimplementing the .NET backend**, not porting the engine.
- RTTI + source-path asserts are present → unusually tractable to reverse.

Start with `docs/00-ARCHITECTURE.md`.
