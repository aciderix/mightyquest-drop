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
- **Routes on the real endpoint pattern** seen in live traffic:
  `/<Service>Service.hqs/<Method>` (GET reads, POST commands; full list in
  `../re/catalog/network/endpoints_observed.txt`).
- **Complete, correctly-typed responses** generated from the reversed catalog
  (`../re/catalog/network/generated/examples.json`): full field sets including
  inherited fields, real enum values, `$type` discriminators. e.g.
  `GetAccountInformation` returns 44 fields with `Privileges: 9` and
  `BuildInfo`/`Wallet`/`ActiveConsumables` present — exactly the fields a prior
  attempt *omitted* (its documented cause of subtle in-game breakage).
- **Stateful** account/session model, persisted to `server/state.json`.
- `/distribution` echoes the client package versions (`package_versions.json`)
  so the patch-check passes.
- **Logs every request** to `server/requests.log` — point the real client here
  and the log captures any method not yet handled, to fill in next.

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
- [x] Validate the wire format offline against the client's real codec
      (`re/tools/validate_codec.py`, Unicorn): both directions proven — int/bool/
      string readers, whole-object `LoginResult` deserialize, `LoginResult`
      serialize, and a serialize→deserialize round-trip (12/12).
- [ ] Account/profile persistence; then the castle/attack loop.

## Legal
Abandoned-game preservation, non-commercial. Ships only our own code + analysis
artifacts — no Ubisoft code or game assets.
