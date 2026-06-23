# The Mighty Quest for Epic Loot — Client Architecture (reverse-engineering notes)

> Status: **recon / static analysis**. Everything here is derived from the
> unpacked PE image `MightyQuest_unpacked_fixed (1).exe` via the tooling in
> `re/tools/`. Reproduce with `python3 re/tools/analyze.py`.

## 1. Binary identity

| Property        | Value |
|-----------------|-------|
| Format          | PE32 (i386), Windows GUI, large-address-aware |
| Linker          | MSVC 11.0 (Visual Studio 2012) |
| Build date      | 2015-07-21 |
| Original PDB    | `D:\HQ\AG_BA073_01\hyperquest\Branches\Update3\Hyperquest\Startup\_Lib\HW_PC_MASTER\Startup\MightyQuest_original.pdb` |
| Project codename| `hyperquest` / `HQ` / `AG_BA073_01`, branch **Update3**, config `HW_PC_MASTER` |
| Code size       | ~10 MB (`.text` 0x9ea14f) |

The image is an **unpacked dump** of an Ubisoft-protected binary. The leftover
`.UBX0` / `.UBX1` sections (entropy ~7–8, i.e. encrypted) are protector
artifacts; `.UBX1` also holds the rebuilt import table. **Caveat:** the import
address table was only partially reconstructed during unpacking — most DLLs list
a single resolved import (see `re/catalog/pe/pe_layout.txt`). IAT repair is a
prerequisite for clean disassembly (see ROADMAP phase 1).

Good news for RE: the build retains **RTTI** (`.?AVInputEngine_Z@@` …) and
**assert strings with full source paths**, so class names, vtables and the
source tree are largely recoverable. This is a far easier target than a stripped
release binary.

## 2. Engine

The game runs on Ubisoft's **Zouna** engine (internal codename **Opal**),
identifiable by the `_Z` class-name suffix convention
(`Camera_Z`, `InputEngine_Z`, `DynArray_Z`, `Singleton_Z`, …) and the
`Opal\Zouna\Engine` source root.

## 3. Module map (game vs third-party)

Generated tally: `re/catalog/pe/module_split.txt`.

**Game code (Ubisoft) — what we care about:**

| Source root                     | Role |
|---------------------------------|------|
| `Hyperquest\Simulation`         | Core gameplay simulation (deterministic combat/world) |
| `Hyperquest\Gameplay`           | Gameplay systems |
| `Hyperquest\BehaviorTree`       | AI / behavior trees |
| `Hyperquest\GameServerProxies`  | **Network protocol** — server RPC proxies + serializers |
| `Hyperquest\Startup`            | Bootstrap |
| `Opal\Zouna\Engine` / `LibPC`   | Zouna engine + PC platform layer |

**Third-party (NOT the game — strip from the game-only view):**

OpenSSL (TLS), libcurl (HTTP), zlib, **FMOD** (audio), **Bink2** (video),
**Recast/Detour** (navmesh/pathfinding), **libCEF/Chromium** (HTML UI),
DirectX 9 (`d3d9`/`d3dx9_43`), MSVC 11 runtime.

## 4. Subsystem → component mapping (from PE imports)

| Subsystem | Implementation |
|-----------|----------------|
| Rendering | Direct3D 9 (`d3d9.dll`, `d3dx9_43.dll`) |
| Audio     | FMOD + DirectSound (`DSOUND.dll`) |
| Video     | Bink2 (`bink2w32.dll`) — cutscenes |
| UI / HUD  | **libCEF** (`libcef.dll`) — the interface is HTML/JS in embedded Chromium |
| Input     | XInput + DirectInput8 (`XINPUT9_1_0.dll`, `DINPUT8.dll`) |
| Net (HTTP)| libcurl over WinHTTP/OpenSSL (`WINHTTP.dll`, `WS2_32.dll`) — `HttpSessionCurl` |
| Net (chat)| **XMPP/Jabber** (`etherx.jabber.org/streams`) — social/chat |
| Platform  | Steam (`steam_api.dll`) |

## 5. Why this matters for a community server

The Mighty Quest was an **always-online** action-RPG. The client is a Zouna
D3D9 app; all persistence, matchmaking, economy, and the attack/defense loop
lived on **Ubisoft's C#/.NET backend**. That backend is gone — which is exactly
what a community revival must reimplement.

Crucially, the client **embeds the entire server contract**:
- 30 RPC **controllers** (`*ControllerBase.cpp`) — the full API surface.
- 100+ assembly-qualified **.NET DTO** type names (`Contracts.Common.*`).
- ~4500 generated proxy/serializer files describing every request/response shape.

So the highest-leverage path to a playable community server is **reversing the
client↔server protocol** (see `01-SERVER-API.md`), **not** porting the renderer.
The engine/renderer only needs to keep working as-is; the server needs to be
rebuilt.

See `ROADMAP.md` for the phased plan.
