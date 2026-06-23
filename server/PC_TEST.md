# Testing on a PC — turnkey

One command launches the game against our local server (fully offline, no remote
backend). It reuses the proven cert/proxy/SSL plumbing from the earlier effort and
serves **complete** responses from our reversed catalog.

## What you need
- The game files (`GameData/Bin/MightyQuest.exe`).
- **Python 3.10+** and **openssl** on PATH.
- **Windows 10/11**, or **Linux/macOS + Wine 7+**.
- This `server/` folder: `mqel_launcher.py`, `mqel_data/`
  (`examples.json`, `package_versions.json`), `plumbing/` (`winhttp.dll`,
  `patch_binary.py`).

## Steps
1. Copy this `server/` folder next to `MightyQuest.exe` (i.e. into
   `GameData/Bin/`) — or run it anywhere and pass `--exe`.
2. Run it (as admin/sudo the first time, so it can edit the hosts file):
   ```
   python mqel_launcher.py
   # or:  python mqel_launcher.py --exe "C:\...\GameData\Bin\MightyQuest.exe"
   ```
3. It will, in order:
   - generate a local CA + server cert for `gs.themightyquest.com`,
   - start an HTTPS proxy on `127.0.0.1:13432` serving our catalog,
   - redirect `gs.themightyquest.com → 127.0.0.1` (hosts file),
   - deploy `winhttp.dll` (redirects the game's HTTP to `:13432`) + `ca.pem`
     next to the exe, and patch the exe's SSL cert path → `MightyQuest_mqel.exe`,
   - launch the game.
4. Watch two logs:
   - `server/mqel_requests.log` — every call the game makes + our response size,
   - the game's `NetworkLog.Txt` (in the game dir) — client-side view.

## Success / iteration
- **Success indicator:** the **hero-selection screen** appears — that means
  `GetAccountInformation` (returning `Privileges: 9` + the full field set) was
  accepted.
- Every `.hqs` method that isn't handled yet shows up in `mqel_requests.log`.
  Send me that log and I add the handler (the response shape is already in
  `examples.json`).

## Notes & troubleshooting
- **SSL:** the exe patch makes the game trust our CA (it loads `ca.pem` next to
  the exe as its OpenSSL trust store). On **Wine**, if it still rejects the cert,
  import the CA once:
  `wine certutil -addstore Root .mqel_certs/ca.pem`.
- **winhttp.dll** is prebuilt in `plumbing/`. If your Wine/Windows rejects it,
  rebuild from source: `cd plumbing && ./build.sh` (needs mingw-w64).
- **Hosts edit needs privileges:** if it prints a line to add manually, add
  `127.0.0.1 gs.themightyquest.com` to your hosts file and re-run.
- **Refresh the catalog** after we improve schemas:
  `cp ../re/catalog/network/generated/examples.json ../re/catalog/network/package_versions.json mqel_data/`
- The game runs unmodified; only a local cert + a winhttp shim + the relative
  cert-path patch are involved. Nothing is sent anywhere — the server is local.
