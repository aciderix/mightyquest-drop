# Automated schema catalog — the whole data model

`re/tools/extract_schemas.py` recovers the JSON field list of **every**
serializable contract in the client, fully automatically (~1 s, no Ghidra).

- Output: `re/catalog/network/schemas.json` (machine-readable),
  `re/catalog/network/schemas.txt` (human-readable)
- Coverage: **2,051 contracts / ~8,400 fields** recovered.

## How it works (manual → automatic)
The first login slice (`04-WIRE-FORMAT-LOGIN.md`) was done by hand. The recipe
turned out to be mechanical, so it was industrialized:

1. Each `*Serializer` registration stub stores its **vtable** — found by
   disassembling the stub (capstone).
2. The vtable's slots point at the serialize/deserialize **methods**.
3. Each method references its JSON **field-name strings** in `.rdata`; we collect
   them by scanning the method's byte range for `.rdata` string pointers.
4. The **contract name** is free, from the stub's source label
   (`FooSerializer.cpp` → `Foo`).

Validation: the automatic output for `LoginResult`,
`GameServerConnectionConfig`, and `AccountLite` matches the hand-reversed
schemas exactly.

## What's in it
Not just network DTOs — the client embeds the server's entire contract model,
including game-tuning settings. Examples:

- **PvP loop**: `CastleInfo`, `AttackInfo` (loot, trophies, treasure room, …),
  `BattleLog`, replays.
- **Economy/items**: `Inventory*`, `Forge*`, `Shop*`, `Wallet*`, item templates.
- **Castle building**: `Castle*` (140+ types — rooms, traps, creatures, layout,
  renovation, validation).
- **Design data**: `AttackSettings`, `AttackerRewardSettings`, `VisualBuildSettings`,
  etc. — the actual gameplay tuning the server shipped to the client.

## Typed schemas (`extract_typed_schemas.py`)
A second automatic pass adds **field types** by walking each contract's
*serialize* method and pairing every `writeKey("Field")` with the value-writer
call that follows it. The writer primitives were named by decompiling them once:

| writer VA | type | how identified |
|-----------|------|----------------|
| `0x009aad80` | `int` | login slice |
| `0x009ab060` | `string` | login slice |
| `0x009ab3f0` | `bool` | writes the literal `"false"` |
| `0x009aae20` | `float` | formatter handles `"toobig"` |
| `0x009aae70` | `datetime` | ISO-8601 format `%04d-%02d-%02dT%02d:%02d:%02dZ` |
| `0x009aa*` (other) | `number` | scalar primitive band, exact width unresolved |
| outside the primitive band | `object` | per-contract nested object/array writer |

Both the **serialize** (writer) and **deserialize** (reader) methods are walked,
so request and response contracts are typed. Reader primitives were named the
same way (e.g. `0x009a8c90` = bool — emits `Expected [true] or [false]`;
`0x009a9170` = duration — parses a `D` suffix and ×86400).

Output: `re/catalog/network/schemas_typed.json` / `.txt` —
**1,325 contracts, 5,461 typed fields** (int 2244, object 1038, string 752,
bool 659, number 447, float 242, datetime 60, duration 19). Validated on
`LoginResult`, `GameServerConnectionConfig`, `CastleInfo`.

### Request vs response (protocol direction)
Each contract carries a `direction`, from which method(s) exist:
- **`request`** (479) — has a serialize method only → client→server.
- **`response`** (56) — deserialize only → server→client (e.g.
  `GameServerConnectionConfig`).
- **`both`** (790) — round-trips in both directions.

`schemas.json` (names only) still has the widest coverage (2,051); the typed
catalog covers the subset whose serialize/deserialize shape was recognised.

## Offline validation against the real codec
The recovered format is not just read statically — it is **executed**: 
`re/tools/validate_codec.py` runs the client's own serializer/deserializer under
Unicorn and round-trips values through them (no game, no Windows). The
`LoginResult` and `AccountLite` boot/login messages round-trip cleanly in both
directions (real deserialize in, real serialize out, values preserved).

**Mass validation** — `re/tools/autovalidate.py` scales this to the whole
catalog automatically: for each two-way contract it *discovers* every scalar
field's object offset by emulating the real deserialize with a memory-write hook
(observing where each value lands), then round-trips the assembled object back
out through the real serialize. Result: **211 / 218 two-way scalar contracts
(96%) round-trip perfectly through the client's own code, both directions**; the
6 incomplete are offset-discovery gaps and the 1 mismatch (`DoorStateTriggers`)
is a known UI-event edge case. See `re/catalog/network/roundtrip_report.txt`.
Contracts with nested-object fields are covered by the static consistency check
above. (Key harness detail: the codec's char-advance and writer primitives are
`stdcall`, so the intercept layer pops their callee args — `emu.py`
`intercept_cleanup`.)

## Exhaustive write/read consistency (`validate_consistency.py`)
A single wrong field — something one side sends that the other can't read — is
what eventually breaks an online client/server. To guard against that across the
*whole* protocol, this tool checks, for every two-way contract, that the client's
**serialize** (what it writes) and **deserialize** (what it reads) agree on field
names and types.

Result: **780 / 790 two-way contracts (98%) are fully write/read consistent**.
The remaining 10 were each examined in the decompiler and are **all false
positives**, not protocol bugs:
- the 3 "type" diffs (`TrapName`, `Name`, `SpecialMessage`) are enum/id fields
  present on *both* sides — only this tool's int-vs-string classifier disagrees;
- the 7 "written-not-read" fields are `EventArgs` base-class fields (e.g. `Id`)
  or client-internal UI view-models (`TooltipModel`, `ForgeModel`, …) — not
  server messages.
So for the actual account/castle/attack/inventory protocol, write/read
consistency is **effectively 100%**. See
`re/catalog/network/consistency_report.txt`.

(Type comparison treats numeric widths as one, and tolerates the reader side
under-detecting nested objects / datetimes, whose readers fall in the numeric
band — a tooling limit, not a protocol mismatch.)

## Caveats / next refinements
- The `number` band groups numeric widths (int64/uint/float32/…) not yet split.
- Nested `object` fields are linked to their child contract by matching the field
  name to a contract name.
