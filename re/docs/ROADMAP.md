# Roadmap — from binary to community server

The goal is a playable community revival. The renderer/engine already works
(it's in the client); what's missing is the **server**. The plan is therefore
ordered to reach a *bootable, login-able* client against a community backend as
early as possible, deferring deep engine RE until it's actually needed.

## Phase 0 — Recon (DONE)
- [x] PE layout, sections, imports, entropy → `re/catalog/pe/pe_layout.txt`
- [x] Identify engine (Zouna/Opal) and tech stack
- [x] Separate game code from third-party libs → `re/catalog/pe/module_split.txt`
- [x] Reconstruct game source tree → `re/catalog/pe/game_source_tree.txt`
- [x] Enumerate server API: 30 controllers + 100+ DTOs → `re/catalog/network/server_*.txt`

## Phase 1 — Make the binary analysable  (in progress)
- [x] RTTI class/vtable recovery → 119 classes, 79 vtables (`re/tools/rtti.py`).
- [x] Ghidra 12.x headless analysis set up + running (`re/docs/02-TOOLING.md`).
- [x] Function auto-labeling from source paths scripted (`re/ghidra/ExportAndLabel.java`)
      → emits `re/catalog/functions.csv`.
- [x] Unicorn micro-emulation harness ready (`re/tools/emu.py`).
- [ ] Repair the import address table (the dump only resolved 1 import/DLL).
      This is the remaining blocker for clean cross-references to library/OS calls.

## Phase 2 — Recover the network protocol (highest leverage)
- [ ] Pick the **login/boot vertical slice** and reverse its serializers to get
      exact JSON shapes (`AccountController`, `BootConfig`,
      `GameServerConnectionConfig`, `EnvironmentManager.ServerInfo`).
- [ ] Recover endpoint URLs/verbs from the `Argo`/curl request builders.
- [ ] Document the wire format in `re/docs/02-WIRE-FORMAT.md` (one file per
      controller as they're reversed).

## Phase 3 — Minimal community server
- [ ] Implement a stub backend (any language) answering boot → login → profile.
- [ ] Patch/redirect the client's server URL to localhost and observe progress.
- [ ] Iterate controller-by-controller until the castle/attack loop runs.

## Phase 4 — Engine deep-dive (only as needed)
- [ ] Reverse `Simulation` determinism (needed so server-side battle validation
      and replays match the client).
- [ ] Document asset/package formats (`EngineSettings.Package*`, `CONFIG:>` VFS).

## Dynamic analysis (Unicorn) — when used
The user proposed Unicorn emulation. It is **not** for running the whole game
(it has no D3D9/GPU/OS). Its sweet spot here is **micro-emulation**: lift an
isolated serializer or crypto/auth routine, feed inputs, and read outputs to
confirm a hypothesised wire format or token derivation without a Windows box.
Plan to wire this up in Phase 2 against individual functions, not the full image.

## Legal note
This is interoperability/preservation RE of an abandoned product. Keep the work
clean-room where it matters (document observed behaviour and protocol, avoid
redistributing Ubisoft's copyrighted code/assets). The repo holds *analysis
artifacts and our own reimplementation*, not extracted source.
