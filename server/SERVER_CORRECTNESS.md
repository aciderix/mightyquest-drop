# Making server responses exactly what the game expects

This is the answer to: *"fields are received but some in-game reactions are wrong
(glitches, bad calculations); responses are probably incomplete or malformed, and
I can't find the cause."*

## Why it happens (the silent-default trap)

The client deserializes each contract **field by field**. A field that is
**missing**, **wrong-typed**, or sent as an **enum name instead of its integer**
does **not** raise an error — the client leaves it at its default
(`0` / `""` / `false` / `null`) and keeps going. Gameplay code downstream then
computes on that default → wrong damage/cost/state, stuck flows, desyncs. Nothing
logs an error. A hand-written response is almost always incomplete, so the bug is
invisible and everywhere.

The contract the game expects is already reversed from the client's own
(de)serializer: `re/catalog/network/schemas_typed.json` (1307 contracts, typed).
**Never hand-write a response — generate it from the catalog and prove it
complete.**

## Response envelope (confirmed against our captured real traffic)

Every game-server reply is wrapped — it is NOT the bare contract:
- reads (e.g. `GetAccountInformation`, `GetCastleInfo`) -> `{"Result": <contract>}`
- things that emit notifications (e.g. `EndAttack`) -> `{"Notifications": [...], "Result": <contract>}`
- `SendCommands` -> `{}` when nothing happened, else `{"Notifications": [...]}`

This is verified from our own `real_traffic.log` ground truth (not the old
project). `stub_server.envelope()` applies it; sending a bare contract is wrong.

## The two guards (host-agnostic, pure Python — run anywhere)

### 1. `completeness_gate.py` — every response is schema-complete
```python
from completeness_gate import Gate
gate = Gate()
body = gate.complete("AccountInformation", body)   # fill ALL fields, recurse nested
issues = gate.validate("AccountInformation", body)  # [] == safe to send
```
- Fills every field with the correct typed default; **recurses into nested
  contracts** so `BuildInfo`, `CastleStats`, `Wallet`… are populated instead of
  left `{}` (the empty-nested-object trap).
- `validate()` reports three categories:
  - `MISSING f` — field absent (the main bug class),
  - `WRONGTYPE f` — type mismatch,
  - `ENUM-NAME f` — an enum sent as its **name**; the client wants the **integer**.
- CLI: `--self-check` (audit the catalog examples), `--trace trace.jsonl` (audit a
  captured session), `--show Contract` (print the complete skeleton).

Wired into `stub_server.py`: `contract()` now runs every response through the gate.

### 2. `command_notifications.py` — `SendCommands` returns the right notifications
The command bus is the #1 suspect for bad calculations: the client posts
`*Command`s and applies the `*Notification`s the server returns to mutate local
state (wallet, inventory, hero xp, buildings). Returning `{}` for a command that
should emit a notification silently desyncs the client.
```python
from command_notifications import CommandBus
bus = CommandBus()
response = bus.handle(request_json)   # {"commands":[...]} -> [notifications] or {}
```
- Maps each of the 53 commands to its notification(s), builds them
  schema-complete with `$type` discriminators and sequential `Index`.
- Fire-and-forget commands (`Tracking`, `ClientIdle`, `*Viewed`, `Set*`) correctly
  produce **nothing**.
- Coverage today: **16 exact, 29 heuristic, 8 unknown** (the 8 are castle-editor
  commands). The full table: `command_notifications.py --table`, and the JSON
  artifact `re/catalog/network/generated/command_notifications.json`.

Wired into `stub_server.py`: `SendCommands` now calls `BUS.handle(req.json)`.

## Confidence — what's exact vs what to confirm

- **Exact (from the client's code):** every notification/contract **shape**
  (fields + types), and the contract for each known endpoint. The codec is
  byte-validated both directions by `re/tools/validate_codec.py`.
- **To confirm against a real capture:** the `~ heuristic` and `? unknown`
  command→notification edges (the *routing*, not the shape), and the integer
  values behind enum names (`enum_values.json` lists members but not reliable
  integer values).

## The loop to reach "no problem at any point in the game"

1. **Generate, never hand-write** — every response from the catalog via `contract()`.
2. **Gate as a hard check** — no response leaves with `MISSING`/`WRONGTYPE` issues.
3. **Capture a full real session** (tutorial → hero pick → castle → PvE/PvP →
   forge → shop → castle edit → events) and run `validate_trace.py` /
   `completeness_gate.py --trace` on it. Every new method or any defaulted field
   shows up → fill it from the catalog.
4. **Confirm command routing** — replace each `~`/`?` edge with what a real server
   returns for that command, observed in the capture.
5. **Resolve enum integers** — for the `ENUM-NAME` fields, send the int the client
   expects (needs the enum value tables; members are in `gamedata/enum_values.json`).

Hosting: `stub_server.py` is a dependency-free Python HTTP server — run it locally
or behind any reverse proxy in the cloud; nothing here is tied to a specific
provider.
