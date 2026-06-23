# Server API surface (community-server target)

> Source of truth: `re/catalog/network/server_controllers.txt` (30 controllers) and
> `re/catalog/network/server_contracts.txt` (100+ DTOs), extracted from the client's
> embedded `GameServerProxies` code.

The client talks to the backend through generated RPC **controllers**. Each
`*ControllerBase` is a service the community server must provide. Grouped by the
game loop:

## Account / session
- `AccountController`, `AccountCreationController` — login, account lifecycle
- `ProfileController` — player profile, progression
- `AvatarController` — player avatar
- `LobbyController` — session/lobby, matchmaking entry point

## Castle defense loop ("build your castle")
- `BuildingController`, `BuildingNavBarController` — place/upgrade defenses
- `CastleInventoryController` — castle contents
- `BuildController` — build/edit operations
- `HarvestingController` — resource harvesting
- `ThemeController` — castle themes/cosmetics

## Attack loop ("raid other castles")
- `AttackController`, `AttackSelectionController` — pick & run attacks (PvP)
- `BattleLogController` — attack/defense history
- `ReplayController` — battle replays

## Heroes / loot / items
- `HeroController`, `HeroInventoryController` — heroes & their gear
- `InventoryController` — global inventory
- `ForgeController` — crafting/forging
- `ConsumableController`, `BuffController`, `SpellController` — abilities/consumables
- `ObjectiveController` — quests/objectives

## Economy & social
- `ShopController`, `WalletController` — store, soft/hard currency
- `FriendshipController` — friends
- `ChatController` — chat (paired with XMPP transport)
- `NewsController` — in-game news feed
- `SeasonalCompetitionController`, `UbisoftCompetitionController` — leaderboards/events

## Transport & serialization
- HTTP via libcurl/OpenSSL (`HttpSessionCurl`), `Argo` networking subsystem.
- JSON payloads built by `HyperquestJsonSerializerFactory`; every contract has a
  matching `*Serializer.cpp` in the client → the wire format is fully recoverable.
- Real-time chat/presence over **XMPP/Jabber**.
- Environment/routing described by `Contracts.Common.EnvironmentManager.*`
  (`ServerDefinitions`, `ServerInfo`, `Branch`) and bootstrapped by
  `Contracts.Common.GameLaunchConfig.*` (`BootConfig`, `GameServerConnectionConfig`,
  `SimulationLaunchConfig`, `CastleGameStateConfig`, `AttackGameStateConfig`, …).

## Next concrete steps to recover the protocol
1. Disassemble the `*Serializer` routines for one vertical slice (e.g. login:
   `AccountController` + `BootConfig` + `GameServerConnectionConfig`) to recover
   exact JSON field names, types and ordering.
2. Recover endpoint URLs/verbs from the controller dispatch tables (look for the
   base URL config near `EnvironmentManager.ServerInfo` usage and the `Argo`
   request builders).
3. Stand up a stub server answering the boot/login sequence and observe how far
   the client progresses (see ROADMAP phase 3).
