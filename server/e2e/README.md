# Headless end-to-end test harness (game ⇄ server, under Wine)

Goal: run the **unmodified** Mighty Quest client headless on Linux (Wine + Xvfb,
no GPU), point it at our local community backend, and **monitor both sides of
every exchange** to prove the client and server communicate correctly.

This folder is the turnkey harness plus the captured evidence and the analysis.

## TL;DR result (2026-06-20, Ubuntu 24.04, Wine 9.0)

| Stage | Status | Evidence |
|---|---|---|
| Wine 32-bit installs, runs the game headless | ✅ | `evidence/MQLog.txt` |
| Game boots: engine, CEF (HTML UI), **D3D9 software render** | ✅ | `MQLog` `DIRECTX: DEVICE RESET SUCCEED!` |
| Game data (Bigfiles, 1.1 GB) loaded via git-lfs | ✅ | no more `Wrong version of bigFile` |
| Hostname redirect + local backend reachable | ✅ | Bloomberg telemetry **connected to `127.0.0.1:13432`** |
| SSL: client's static OpenSSL trusts our CA | ✅ | CA placed at `/usr/local/ssl/cert.pem` (= Wine `Z:`) |
| winhttp cert-bypass shim loads | ✅ | `evidence` `winhttp_proxy.log` |
| Server wire format == client's real codec | ✅ | `validate_codec.py` → **2/2 round-trip both directions** |
| **Client reaches the HTTP game-API (`GetAccountInformation`)** | ⛔ | blocked by the crash below |

**One client-side blocker remains:** the game crashes **deterministically** at
the `LoadGameSettings` boot step, *before* it issues the HTTP game-API calls.

```
Bloomberg: Exception Caught at 0x00908690 (Violation when reading address 0x00000060)
MQLog last line: SCRIPT  LoadGameSettings
```

Root cause (static analysis, see "Diagnosis"): the `LoadGameSettings` handler
`FUN_00908440` reads `this->[0x1c50]` (the parsed GameplaySettings source
object) which is **NULL**, then dereferences `null+0x60`. i.e. the local
`Data/GameplaySettings/settings.bin` was not deserialized into the settings
object on this build/Wine combo. This is a **client/data** issue, independent
of the server — the network layer is already up at this point.

## Run it

```bash
sudo bash run_e2e.sh 150        # bring up backend + plumbing, launch game 150s
python3 validate_trace.py       # validate captured exchanges vs schema catalog
```

## Files

- `monitor_server.py` — instrumented backend. Listens HTTP `:80/:8080` + HTTPS
  `:443/:13432`, routes `/(Service)Service.hqs/(Method)` via the reversed
  catalog (`examples.json`, 1307 contracts), returns `Privileges:9`, and logs
  **every** exchange (method/path/headers/body ↔ response) to `trace.jsonl`.
- `run_e2e.sh` — turnkey: CA → `/usr/local/ssl/cert.pem`, `/etc/hosts` redirect,
  deploy winhttp shim + ca.pem, start backend + `tcpdump`, launch game headless.
- `validate_trace.py` — per-request schema-completeness check + endpoint coverage
  vs `endpoints_observed.txt`.
- `certs/` — local CA + `gs.themightyquest.com` server cert (SAN-correct).
- `evidence/` — `MQLog.txt`, `HQ_Bloomberg.log` from a real run.

## How the redirect works (what the game actually does)

The client's API transport is **libcurl + statically-linked OpenSSL** (`Argo /
HttpSessionCurl`), not WinHTTP. Three things make an unmodified client talk to us:

1. **Hostname** — `/etc/hosts: gs.themightyquest.com → 127.0.0.1`. Wine uses the
   host resolver, so this is honoured (confirmed: Bloomberg resolved and
   connected to `127.0.0.1`).
2. **TLS trust** — the static OpenSSL was built with `OPENSSLDIR=/usr/local/ssl`
   and loads `/usr/local/ssl/cert.pem`. Under Wine the `Z:` drive maps to Linux
   `/`, so dropping our CA at the real `/usr/local/ssl/cert.pem` makes the
   unmodified, *packed* exe trust our cert — no binary patch needed (the
   `plumbing/patch_binary.py` patch is only for native Windows).
3. **WinHTTP** — a few components use WinHTTP; the `plumbing/winhttp.dll` shim is
   loaded (`WINEDLLOVERRIDES=winhttp=n,b`) and forces `IGNORE_*` cert flags.

## Next step to finish e2e

Get past `LoadGameSettings`: reverse how `[manager+0x1c50]` (the GameplaySettings
object) is populated from `settings.bin`, or feed settings the game accepts.
Once the boot proceeds, the very next thing the client does is
`GET /AccountInformationService.hqs/GetAccountInformation` — which the backend
already answers correctly (44 fields, `Privileges:9`), and `validate_trace.py`
will then light up with the live exchanges.
