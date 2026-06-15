# Real traffic & prior work — findings (from the community-server attempt)

A previous community-server effort (private repo
`The-Mighty-Quest-For-Epic-Loot-port`) left **real client↔server network logs**
(~475 KB, 79 exchanges) plus its own schema extraction. The raw logs / that repo
are not copied here (they contain another deployment's tokens/infra); this file
records the **useful facts** for our spec. The runtime *values* came from a
hand-made, partly-buggy server — treat values as indicative, not authoritative;
the **routing and message shapes are ground truth** (the client is unmodified).

## 1. Endpoint routing (fills the static-analysis gap)
The Argo routing we could not fully resolve statically is, from real traffic:

    <VERB> /<Service>Service.hqs/<Method>      GET = read, POST = command/mutation

Observed routes are in `re/catalog/network/endpoints_observed.txt`
(`/AccountInformationService.hqs/GetAccountInformation`,
`/HeroService.hqs/ChooseFirstHero`, `/AttackService.hqs/StartAttack|EndAttack`,
`/CastleForSaleService.hqs/...`, `/AccountService.hqs/ChooseDisplayName`, …).

**Command bus:** `POST /ServerCommandService.hqs/SendCommands` carries a batch of
`*Command` objects (Tracking, ClientIdle, Buy*, HeroEquip*, InventoryMoveItem,
Logout, …); the server replies `{}` or a list of `*Notification` objects.

## 2. Cross-validation of our schemas
30 / 32 contract `$type`s seen in real traffic are present in our catalog (only
`GameInitializeTracking`, `LogoutCommand` were missing — trivial marker types).
The real messages use the same `$type` discriminator and field names our typed
schemas describe → independent confirmation that the reversed protocol is correct.

## 3. Why their build had in-game bugs (root cause → our fix)
Their own `log_vs_schema_analysis` flagged that the server's **responses were
incomplete** vs the expected schema, e.g. `GetAccountInformation` was **missing
32 fields** (`BuildInfo.*`, `Wallet.InGameCoinStorageCapacity` /
`LifeForceStorageCapacity`, `ActiveConsumables`, `Guild`, `Expirables`,
`CompletedAchievements`, `Stats.*`, …); `ChooseFirstHero` missing `EquippedSpells`,
`HeroStatModifier`, … A missing field → the client falls back to a default →
subtle breakage (their "can't leave combat"-style bugs). This **confirms the
"emit every field" rule** and is exactly what our now-complete schemas address:
inheritance recovery + game-data merge brought us to **0 missing fields vs the
game data** (see `05-SCHEMA-CATALOG.md`), so a server generating responses from
our catalog won't omit those.

## 4. Useful constants & mechanics (observed)
- New-account gate: `GetAccountInformation` must return `Privileges: 9` or the
  hero-selection screen never appears.
- Currency ids: `PremiumCash = 1`, `Gold = 2`, `LifeForce = 4`.
- `GameStateType` values seen: 2, 5 (state-machine in `GameStateTracking`).
- Hero choices: Knight / Archer / Mage / Runaway (`ChooseFirstHero`).
- **SSL caveat:** the client's 2014 libcurl can't verify modern certs, so a
  **local HTTP proxy** is used to bridge to an HTTPS backend (the client itself is
  unmodified). Relevant when pointing the client at any modern server.

## 5. Related external RE (public)
- `widberg/ImZouna` — ImHex hex patterns for **Zouna** data structures, incl.
  `patterns/mqfel/` (BFPC, SettingsBin, StreamingAudio) — useful for the packaged
  asset / settings-binary formats (`.zou`, PackagesTOC, `settings2` decryption).
- `SabeMP/zouna-templates-docs`, `widberg/fmtk` — Zouna format docs / toolkit.
