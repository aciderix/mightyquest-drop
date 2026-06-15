# Mighty Quest — community server (stub)

First iteration of a community backend for *The Mighty Quest for Epic Loot*.
The original game was always-online against Ubisoft's (now-gone) C#/.NET servers;
this reimplements that backend. See `../re/docs/` for how the protocol was
reverse-engineered.

## Run it (zero dependencies)
```bash
python3 server/stub_server.py --host 0.0.0.0 --port 8080
```
Python 3 standard library only — runs on the same machine as the game, or on a
VPS for online hosting.

## What it does now
- **Stateful** account / session / profile model, persisted to
  `server/state.json`: login finds-or-creates an account for a Steam ticket,
  issues a `ConnectionToken`, and the profile/account handlers resolve the
  session by token (`Authorization: Bearer <token>`).
- Answers the **boot / login** sequence with correctly-shaped JSON
  (`BootConfig`, `ServerDefinitions`/`ServerInfo`, `GameServerConnectionConfig`,
  `LoginResult`, `AccountLite`).
- For any other request, serves the matching contract's example payload
  (from `re/catalog/network/generated/examples.json`, 1,325 contracts) or `{}`.
- **Logs every request** (method, path, content-type, body) to stdout and
  `server/requests.log`.

That last point is the important one: point the real client here and the log
captures the **exact URLs, verbs and bodies** it sends — that is how we pin down
the real `Argo` routing that static analysis can't fully resolve yet.

## Pointing the client here
The client reads its entry config from `BootConfig` /
`GameServerConnectionConfig` (a `DistributionServiceUrl` / `GameServerUrl`).
Redirect those to `http://<this-host>:<port>` — by editing the client's local
config, or DNS/hosts redirection of the original hostname. (Requires the runnable
game on a Windows box; the analysis dump in this repo does not execute.)

## Status & roadmap
- [x] Boot/login shaped responses + universal request logging.
- [ ] Replace example payloads with real per-controller logic, guided by the
      captured request log + the typed schemas.
- [~] Validate response shapes offline against the client's real deserializer
      (`re/tools/validate_codec.py`, Unicorn): integer reader proven end-to-end;
      bool/string readers WIP (more parser-context emulation needed).
- [ ] Account/profile persistence; then the castle/attack loop.

## Legal
Abandoned-game preservation, non-commercial. Ships only our own code + analysis
artifacts — no Ubisoft code or game assets.
