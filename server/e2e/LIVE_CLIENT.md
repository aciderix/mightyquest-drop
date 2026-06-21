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

## Remaining blockers (in boot order)

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
