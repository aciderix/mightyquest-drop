# Driving the live client headless (Wine + CEF UI) — findings & recipe

Goal: run the real game headless and control/inspect its UI programmatically, to
test server↔client end-to-end against our local server.

## UI technology (confirmed)

The game UI is **HTML/CSS/JS rendered in CEF 3.1453.1255 (Chromium 28, 2013)**:
- `Bin/libcef.dll` (FileVersion 3.1453.1255), `Bin/mightyquest-ui.exe` (CEF subprocess),
  `Bin/libEGL.dll`/`libGLESv2.dll`.
- UI source on disk: `Data/UI/Html/<locale>/Index.html` + `TopView.html`, classic
  jQuery 1.7.2 / underscore / jsrender app with generated controllers
  (`Js/generated/controllers/hyperquest.controller.*.js`) and a `Facade.js` manager.
- Engine↔UI bridge: `CEFClient_Z` (`sources\CEFClient_Z.cpp`).

Two ways to drive it:
1. **CDP (Chrome DevTools Protocol)** via `--remote-debugging-port`. The switch IS
   accepted (logged as `COMMANDLINE:--remote-debugging-port=9222`) and CEF
   initializes, but the DevTools port never bound reachably in testing (CEF
   likely runs with `command_line_args_disabled`, or the port isn't propagated to
   CefSettings). Would need a libcef shim to force `remote_debugging_port`.
2. **Injected JS control agent (recommended)** — we own `Data/UI/Html/...`, so add
   a `<script>` that opens a WebSocket (Chromium 28 supports WS) to a local Python
   "director". It can then read the DOM, call `hyperquest.controller.*`, dispatch
   clicks — no dependency on CEF remote debugging or struct offsets.

## Wine launch — the KEY fix: Windows version = 7

Without it the client **crashes** during `LoadGameSettings`:
`Exception at 0x00908690 (read address 0x60)` — a bad-pointer deref in the
gameplay-settings loader (settings live in `Data/GameplaySettings/settings.bin`).
The crash is environment-specific (Wine), not missing data.

```sh
export WINEPREFIX=/home/user/wineprefix WINEARCH=win32 DISPLAY=:77
wine reg add 'HKCU\Software\Wine' /v Version /d win7 /f      # <-- the fix
Xvfb :77 -screen 0 1280x1024x24 &
cd /home/user/port/GameData/Bin
WINEDLLOVERRIDES="winhttp=n,b" CURL_CA_BUNDLE='Z:\usr\local\ssl\cert.pem' \
wine MightyQuest.exe -server_url https://gs.themightyquest.com \
  -environmentName mqel-live -branchName mqel \
  -steamid 76561201696194782 -steamticket "" -token ""
```
With `winver=win7` the client boots far: DirectX device-reset OK → CEF init + 2
RegisterView → gameplay settings load (~969 log lines, benign `IsVisible` JSON
warnings) → loading screen → **plays the intro Bink movie** (`Data/Movie/
Ubisoft_Logo.bk2` via `bink2w32.dll`) → `WaitPlayingMovieEnd`, then exits.

## Rendering: DXVK + lavapipe (works)

No GPU in the container, but software Vulkan (Mesa lavapipe, `libvulkan_lvp.so` +
`lvp_icd.json`) is present. DXVK 1.10.3 `d3d9.dll` (32-bit) dropped into the prefix
runs the game's D3D9 on Vulkan/lavapipe:
```sh
# install DXVK d3d9 into the 32-bit prefix
cp dxvk-1.10.3/x32/d3d9.dll  $WINEPREFIX/drive_c/windows/system32/d3d9.dll
# launch with:
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json
export WINEDLLOVERRIDES="winhttp=n,b;bink2w32=n;d3d9=n"
```
Confirmed working: DXVK creates its device/state cache, the D3D9 cap checks pass,
CEF registers views. Rendering is NOT the boot blocker.

## Fonts

The prefix shipped with zero fonts. Installed system TTFs + `winetricks -q
corefonts` (Arial/Times/Verdana/…). Does NOT change the InitFonts crash below.

## Remaining blocker: deterministic crash 0x009CA2AF in InitFonts

After winver=win7 (settings) + bink stub (movie) + DXVK (render) + corefonts, the
client reliably reaches font/UI init (`OpenOpalPanel: LoadingPanel`,
`Source DB:>Scripts>InitFonts.tsc`) and then crashes — **deterministically, same
address every run**: `0x009CA2AF reading 0xFFFFFFF4`.

Disassembly (unpacked image):
```
0x9CA2A0  getEntry(index): mov eax,[ebp+8]      ; index
          lea edx,[eax+eax*4]                    ; index*5
          mov eax,[ecx+0x80]                      ; this->table  == NULL
          mov eax,[eax+edx*8+0x1c]                ; table[index*40+0x1c]  -> FAULT
```
The fault address 0xFFFFFFF4 decodes to `index = -1`, `table = NULL`: an earlier
**lookup returned "not found" (-1)** and the manager's table at `this+0x80` was
never allocated, then this getter indexes it unchecked. It is NOT rendering (same
under DXVK and WineD3D), NOT data (all 51 bigfiles present, 893 MB), NOT the movie
(passed), NOT font-presence (corefonts installed). It is an engine resource/tag
lookup that fails under Wine during UI/font init. Fixing it needs either deep RE
of the failing lookup (what name/tag isn't found) or a runtime null-guard patch
(hard: the shipping exe is packed, so patches must target the in-memory image).

## Steam re-download: blocked in this container

`steamcmd +login` fails with `CreateBoundSocket: failed to create socket,
EAFNOSUPPORT` even with the sandbox disabled — the container network policy allows
HTTP(S) (curl works) but not Steam's socket protocol. A clean copy would have to be
fetched on a normal machine. (It likely would not fix 0x009CA2AF anyway: same
binary + the present data already reproduces it.)

## Original blockers (now resolved)

1. **Intro Bink movie** (`WaitPlayingMovieEnd`). Disabling `bink2w32` or truncating
   the `.bk2` both **crash** (the engine requires a valid movie). Need a real
   skip: a minimal valid `.bk2`, a `bink2w32` stub that fires the end callback, or
   the engine's `IsMovieSkippable` / `MovieStoppedAssignmentTrigger` path.
2. **Login handshake to a local server.** The bare `MightyQuest.exe` path that
   boots uses real SSL (`CURL_CA_BUNDLE`); our server must present a trusted cert
   for `gs.themightyquest.com` and the host must resolve to localhost.
   `mqel_launcher.py` sets up cert+proxy+hosts+winhttp shim but launched a patched
   `_mqel.exe` with `winhttp=n` (no `,b`) and no `CURL_CA_BUNDLE` and did not boot —
   reconcile it with the working direct recipe above.
3. **Software-render nondeterminism.** No GPU; Wine uses Mesa software GL. Runs
   reach slightly different points (191 / 963 / 969 lines) — needs a stable
   render path (llvmpipe tuning) or retries.

## Server communication mechanism (from the reference project, port/)

- **C++ era (`MQELOffline_cpp`, Ayria framework):** in-memory patch — injected DLLs
  (`Localbootstrap.dll` + `Localnetworking` `.ayria32` + `MQELOffline` `.LN32`) hook
  the game at the socket level (Patternscan/Hooking) and an in-process C++ HTTP
  server answers the `.hqs` endpoints; fake `steam_api.dll` for Steam auth. Fully
  offline.
- **Supabase era (`server/launcher.py`):** no disk patch — native `-server_url` +
  a JWT `-token`, talking real HTTPS to a cloud edge function. (This is the version
  that had the in-game bugs — hand-written, incomplete responses.)

`port/` is reference only; our truth is `re/catalog/network/` + `real_traffic.log`.

## Note on real_traffic.log provenance

It is a copy of the user's own capture against their (buggy) server. So:
**client REQUESTS = truth** (formats, command batches, and — where present — the
sequence); **server RESPONSES = informational** (their server's, not authoritative
for field completeness). The `{Result/Notifications}` envelope is reliable because
the real client accepted it. The capture starts post-login (first entry is an
in-game `SendCommands`), so it does NOT contain the boot/login sequence.
