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

## Update: crash registers + Steam via DepotDownloader

Crash 0x009CA2AF register dump (WINEDEBUG=+seh): `ecx=06401e18` (the glyph
manager — a VALID object), `[ecx+0x80]=NULL` (its glyph table was never
populated), `edx=fffffffb` (index = -1). So the font manager is constructed but
its glyph table is empty under Wine → text layout looks up a glyph, misses (-1),
and indexes the null table. Root cause needs a runtime backtrace of the
font-package load (the manager exists; its table just never fills).

Steam: `steamcmd` is blocked (EAFNOSUPPORT), but **DepotDownloader connects**
(self-contained linux-x64 build, no dotnet needed) — it reaches Steam over
WebSocket/443 (Steam api/cdn are reachable here). Login gets to Steam Guard 2FA;
provide the emailed code to fetch a clean copy (app 239220) and rule out / fix
any missing bigfiles.

## DEFINITIVE: GitHub copy is complete; crash is purely Wine

Downloaded a pristine copy via **DepotDownloader** (app 239220, depots 239221 +
239222, 1.4 GB) — it connects over WebSocket/443 where steamcmd fails
(EAFNOSUPPORT). Comparison vs the repo's game copy:
- 0 files present in the clean copy but missing from the repo copy.
- 52/52 BFPC bigfiles match; `MightyQuest.exe`, `PACKAGE_3236A0AB_AI739.BFPC`
  (UI fonts), `settings.bin`, `libcef.dll` are **byte-identical (SHA256)**.

So the data is complete and correct. The 0x009CA2AF InitFonts crash is **purely a
Wine compatibility issue** (the glyph manager exists but its table never fills
under Wine — most likely a load-order/timing difference, since data + parsing are
identical to a working install). A clean copy does not change it. Path forward:
a winedbg backtrace of the font load, a different Wine build/config, or running on
real Windows / a GPU host (where this user's install previously reached the game).

## DEEP DIVE: the InitFonts wall is the glyph subsystem (exhaustively proven)

After clearing every other wall, the client boots stably under Wine
(`win7` + bink-skip stub + DXVK/lavapipe + clean `/tmp/.wine-*` sockets) all the
way to **GameplaySettings load / InitFonts**, then hits the glyph manager.

What was tried and learned (minidump backtrace + register dumps):
- Crash `0x009CA2AF` is `glyphMgr.getEntry(idx)` with `this->table` (`+0x80`) NULL
  and `idx=-1`; backtrace: `getEntry` <- `getGlyphMetric 0x9D8720` <- text-layout
  loop (`0x995…/0x991…/0x99c…`) rendering the loading-screen string. The manager
  object is valid but its glyph table never fills (font package not loaded in time).
- Byte-patching `getEntry` to guard the NULL (incl. the missing `pop ebp`) clears
  that site but the same manager has more NULL fields (`+0x2f0`, vtable) → cascade
  (`0xA06100 mov esi,[edx]`, `0xA06102 push [..]`, `call [esi+0xe8]`).
- A vectored exception handler (`binkstub` `veh`) that skips NULL-deref
  `mov/push/call` (zeroing dest / pushing 0) **stops all the crashes** — the
  process stays alive (procs=4, no new crash for minutes) — BUT zero-width glyphs
  make the text-layout loop **never terminate** (99% CPU, MQLog frozen mid
  GameplaySettings); scoping the VEH to the font range only doesn't help.

Conclusion: the glyph subsystem genuinely needs the font atlas loaded — it can't
be crashed-through or faked (NULL → crash, zero → infinite layout). The font
package (`PACKAGE_3236A0AB_AI739.BFPC`, present and byte-identical to the Steam
copy) does not get parsed into the manager under this headless Wine. That is the
one remaining blocker. It loads fine on real Windows (where the user's install
previously reached the game), so the realistic path to a live, controllable
client is a Windows/GPU host using this recipe; the headless-Wine path is blocked
at the font loader specifically.

Artifacts: `binkstub/stub.c` (the VEH + bink-skip), `binkstub/initfonts_crash.dmp`
(the minidump with the glyph-manager backtrace).

## Evaluated external suggestions (ChatGPT/Gemini) — results

1. **Dummy glyph with width>0 (not 0)** — tried: VEH special-cased the glyph
   advance-getter `0x9CA2AF` to return 12 instead of 0. Did NOT unblock: the
   stall is not the word-wrap advance loop; the game still freezes mid
   GameplaySettings (the loading-screen render thread spins on the VEH-handled
   faults and starves the boot/script thread).
2. **WineD3D instead of DXVK** — NOT possible in this container: this Wine cannot
   load a builtin `d3d9` (`import_dll d3d9.dll not found`, status c0000135), with
   or without copying its `i386-windows/d3d9.dll` into the prefix. DXVK is the
   only `d3d9` that loads, so WineD3D's GDI/texture path can't be tested here.
3. **winetricks corefonts / tahoma / gdiplus** — corefonts installed, no effect.
   The UI fonts are the game's own baked bitmap atlases (Opal objects in
   `PACKAGE_3236A0AB_AI739.BFPC`, verified by unpacking) — NOT Windows GDI fonts —
   so GDI/GDI+ font generation is not on this path.
4. **WINEDEBUG=+d3d / DXVK info log** — done: DXVK initialises cleanly (v1.10.3,
   BC compression + needed formats present) and reports NO texture-creation
   failure through the font-load point (MQLog 979). So the atlas isn't failing a
   format check; the glyph manager's table is null because the font isn't
   registered/loaded when the loading panel renders text (a load-order/lookup
   issue under Wine), not an obvious texture error.
5. **Xvfb / Device Context** — already in use (all runs are under Xvfb).
6. **Case sensitivity** — the font data is read from the BFPC bigfile by exact
   internal name (other packages load fine), not from loose case-sensitive files.
7. **Real GPU (virgl/passthrough/NVIDIA) or Windows VM** — the correct fallback,
   but unavailable in this GPU-less container (software Vulkan/lavapipe only).

Net: every in-container avenue is exhausted. The blocker is the engine's glyph
manager being empty when the loading screen renders, under headless software
Wine; it crashes (unguarded) or stalls (guarded). A real-GPU host or Windows is
required to validate the live UI; everything else (boot recipe, bink-skip, DXVK,
VEH, minidump backtrace, the entire server-correctness toolchain) is done and
committed.

---

## BREAKTHROUGH 2 — the client boots, connects to our server, and runs (no GPU)

The earlier "net" conclusion was too pessimistic. The glyph wall is **not** the
end: the engine's text rendering is a single class and the network/SSL stack is
fully tractable in-container. The live client now boots to a stable running
state, talks to our local server over TLS, and exchanges real game API calls —
all headless under software Wine. Repro: `start_gameserver.sh` then `launch_lobby.sh`.

### 1. The text-render crash *cluster* — one class, patched wholesale
All boot crashes (27+) were one C++ class: a **shader-based text element**
(vtable `0xF4F1E4`, identifiable by the `"ERROR - Shader <"` string right after
it). Its GPU shader resource lives at `this+0x2f0`, set NULL by the ctor
(`0xA06076`) and only filled when the native shader is created — which never
happens under software rendering. Well-behaved vtable methods guard
`if(this+0x2f0==NULL) return;`; the **draw / build / glyph-lookup** methods don't
and deref NULL (or do a glyph lookup with index −1 → `edi=0xFFFFFFC0`).

Fix (runtime, in the bink stub, applied at movie time after `.text` unpacks):
force each crash-prone method to early-return with the correct stdcall cleanup:
- `0xA060E0` text-DRAW → `xor eax,eax; ret 4`
- `0xA06550`, `0xA065C0` glyph-index lookups → `ret 8` / `ret 4`
- `0xA061D0` Draw, `0xA06250` SetVisible/fade, `0xA06CD0` Build geometry → `ret`
- plus the original `0x991A8A` `je→jmp` (loading-screen text skip)

This skips only **engine-side** text; the real UI is CEF/HTML and renders
independently. Result: boot is **stable, zero crashes**, all the way to the
lobby/controller-init stage.

### 2. Networking — DNS, TLS, and the empty-trust-store
- The game's hard-coded host is `gs.themightyquest.com`. Wine's curl resolver is
  flaky ("timeout on name lookup is not supported"), and the container resets
  `/etc/hosts`. **Fix: launch with `-server_url https://127.0.0.1`** — our server
  cert has `SAN IP:127.0.0.1`, so hostname checks pass and DNS is bypassed.
- Run the catalog server over **TLS on :443** (`gameserver.py`, from
  `mqel_launcher`), CA at `/tmp/ca.pem`.
- **SSL trust:** the game's static **libcurl 7.38** was built with *no* CA bundle.
  With `verifypeer` on (default) and no `CAINFO`, its trust store is **empty** and
  *every* cert is rejected — it never even opens a CA file (confirmed by
  `WINEDEBUG=+file`). No CA path (`SSL_CERT_FILE`, `ca.pem`, patched OPENSSLDIR
  string) can fix this, because curl 7.38 predates `CURL_CA_FALLBACK` and never
  calls `set_default_verify_paths`. **Two runtime patches disable verification**
  (the curl equivalent of the winhttp shim's `IGNORE_ALL_CERT_ERRORS`):
  - `ssl3_get_server_certificate` in-handshake gate `0xAC1803`: `je 0xAC18A0`
    (taken when `verify_mode==NONE`) → unconditional `jmp 0xAC18A0`, so the
    chain-verify result is ignored and `SSL_connect` succeeds.
  - `SSL_get_verify_result` (`0xABE0E0`, `return ssl->verify_result@+0xEC`) →
    `xor eax,eax; ret`, so curl's post-handshake re-check sees `X509_V_OK`.

  Result: `SSL connection using ECDHE-RSA-AES128-GCM-SHA256` → `SSL certificate
  verify ok.` → `HTTP/1.1 200 OK`.

### 3. Confirmed live client↔server traffic
With both in place the client reaches the server and the log shows real calls:
`POST /AccountService.hqs/GetAccountInformation` (→ our 4614-byte
`AccountInformation`), `POST /ServerCommandService.hqs/SendCommands` (len 330),
and a time-sync line `Server … Client … tardiness 0 sec`. **No `ErrorPanel`.**
The game proceeds into `StartInitializeControllerTask` / `Waiting for
AccountServerController` — i.e. the blocker is now pure **server-response
correctness** (drive the lobby flow with complete responses), exactly what
`completeness_gate.py` + `command_notifications.py` + `SERVER_CORRECTNESS.md`
exist for. The crash/SSL/boot walls are gone.
