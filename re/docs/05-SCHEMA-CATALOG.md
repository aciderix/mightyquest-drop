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

Output: `re/catalog/network/schemas_typed.json` / `.txt` —
**1,269 contracts, 5,126 typed fields** (int 2204, object 1016, string 743,
bool 660, float 237, number 204, datetime 62). Validated on `LoginResult`,
`CastleInfo`.

### Request vs response (protocol direction)
The 1,269 typed contracts are exactly those with a **serialize** method — i.e.
the ones the **client emits** (requests / client→server). Contracts that appear
only in `schemas.json` (names) but not in `schemas_typed.json` are
**deserialize-only**: the client only reads them, so they are **server→client
responses/config** (e.g. `GameServerConnectionConfig`). This split tells a
server implementer which side produces each message.

## Caveats / next refinements
- Read-only (response) contracts are typed only by name so far; a symmetric pass
  over the *deserialize* readers (`readInt`/`readString`/…) would type them too.
- The `number` band groups numeric widths (int64/uint/float32/…) not yet split.
- Nested `object` fields are linked to their child contract by matching the field
  name to a contract name.
