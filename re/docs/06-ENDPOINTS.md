# Endpoints & routing model

How the client reaches the backend. Recovered from the boot/connection contracts
(`schemas_typed.json`), the controller proxy methods, and the transport strings.

## Routing is RPC-over-HTTP, not REST
There is **no per-method REST path**. Each `*ControllerBase` method dispatches
through a **vtable slot** (`call [this + 0x34/0x38/0x3c/...]`) into the shared
`Argo` transport, which POSTs a JSON body to the game-server URL. So a method is
identified by its controller + slot/method id inside the RPC layer, not by a URL
like `/profile/get`. The `game://...` strings in the binary are the **CEF UI**
navigation bridge (HTML→native), unrelated to the server API.

Transport facts:
- HTTP via libcurl; payloads `application/json`.
- Auth bootstrapped from a **Steam ticket** (`-steamticket`); the server returns a
  `LoginResult.ConnectionToken` used for subsequent calls.
- Social/chat is separate, over **XMPP** (see architecture doc).

## Boot / connection sequence
1. **BootConfig** (`CONFIG:>Hyperquest>BootConfig.json`) — entry config:
   `DistributionServiceUrl`, `EnvironmentName`, `WorldName`, `GameWebsiteUrl`,
   `PlayerLoadConfig`, `CastleLoadConfig`, latency/patching flags.
2. The **distribution service** returns **ServerDefinitions** →
   `ServerInfos`: a list of **ServerInfo** `{ ApplicationID, DeploymentServiceID,
   RelativePathToApplication, ServerName }`. The service URL is
   `base + RelativePathToApplication`.
3. **GameServerConnectionConfig** (response) → `{ GameServerUrl, AccountName,
   AccountPassword, HttpCompression }` — the resolved game-server URL + creds.
4. Client authenticates → **LoginResult** `{ AccountId, ConnectionToken,
   ProfileId }`; subsequent RPC calls go to `GameServerUrl` carrying the token.

## Controllers = services
The 30 `*Controller`s (`re/catalog/network/server_controllers.txt`) are the RPC
services; each method maps to one request contract (`request`/`both` in
`schemas_typed.json`) and one response contract. Example slice already typed:
- `AccountController` ↔ login → `LoginResult`.
- `AttackController` / `AttackSelectionController` ↔ `AttackInfo`, `CastleInfo`.

## Remaining unknown
The exact on-the-wire method selector (numeric id vs name, and any URL suffix) is
inside the `Argo` request builder reached via the controller vtable slot
(`this->vtable[+0x34]`). Static extraction is costly: the controller public
methods are non-virtual (not found in any vtable), so resolving the send method
means recovering each controller's vtable via its constructor — no RTTI exists
for the `GameServerProxies` classes. The callback object
(`vtable DAT_00f84820`, handler `FUN_00614cf0`) is just request/response
lifecycle, not the route.

**Pragmatic resolution:** the stub server (`server/stub_server.py`) logs every
request, so pointing the real client at it yields the exact URLs/verbs/bodies
empirically — higher ROI than deep static dispatch analysis. Capture first, then
formalise routes from the log.
