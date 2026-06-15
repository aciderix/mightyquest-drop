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

## Precise wire shapes (what makes a message well-formed)
Every scalar serialize/deserialize **primitive** was decompiled and mapped to an
exact **wire shape** — the only thing that decides if a field is well-formed on
the wire:

| shape | on the wire | covers |
|-------|-------------|--------|
| `num` | bare number `42` | int/uint/byte/short/long/ulong/double (buffer widths 4/11/12/22/20 → byte/uint/int/int64/double) |
| `str` | quoted `"..."` | string, **datetime** (ISO-8601), **enum** (`"0x"+16 hex`), guid |
| `bool`| `true`/`false` | bool |
| `arr` | `[ ... ]` | array readers (a `]` branch) + plural field names of a known contract |
| `obj` | `{ ... }` | nested contract |

Corrections that matter for a community server (each a classic silent-break
source) — the precise per-field types live in `schemas_typed.json` and the
non-obvious ones are listed in `re/catalog/network/special_fields.txt`:
- **Enums are a quoted 16-hex-digit string**, e.g. `"0x0000000000000003"` — not a
  bare number and not a readable name. The writer (`009aaf00`) calls
  `FUN_00426f30`, which emits `"0x"` then 16 hex digits of the 64-bit value; the
  reader (`009a8670`) parses that back. A safe default is `"0x0000000000000000"`.
  (56 enum fields.)
- **Datetimes are quoted ISO-8601 strings** (`"2015-06-15T00:00:00Z"`; writer
  `009aae70`, reader `009a8f90`). (76 datetime fields.)
- **Arrays** (`ServerInfos: ServerInfo[]`) are distinguished from single objects.

Numeric width (int/uint/byte/short/long/ulong/double) is captured per field for
value-range validity, though all share the bare-number wire form.

### Structural completeness (inheritance recovery + game-data merge)
The codec walker now **follows base-class delegation**: a serialize/deserialize
method that calls another contract's serialize/deserialize (base class) has those
inherited fields merged in (base first, deduped). This recovered **~1,800 fields**
the per-method walk previously missed (e.g. `DefeatCastleAchievement` now carries
its base `Id`/`Points`/`DescriptionId`/`SteamId`/… — 5,461 → **7,286 typed
fields**). The game-data observed fields are then merged on top.

Cross-checking the result against the real game data: **286 observed fields
confirmed and 0 types with any field missing** (was 32 types with gaps). So for
every contract that also appears in the game data, our schema now has the
complete field set. Structure + types + wire shape + enum values are complete;
only the **runtime values** (which id, which fields populated when) still require
live traffic to pin down.

### Ground truth from the game's own data (`gamedata/`)
The game's `GameplaySettings` JSON (8,726 files, supplied separately — raw assets
not committed) was mined by `analyze_gamedata.py` into derived catalogs under
`re/catalog/network/gamedata/`:
- **`enum_values.json`** — 271 fields with their **real valid values**
  (`BuildingType` = ArchitectOffice/BlackSmith/CastleHeart/…, `CurrencyType` =
  IGC/LifeForce/PremiumCash, `ItemType`, …). `gen_examples.py` now uses these, so
  **264 contracts get a real enum value** in their example instead of a placeholder.
- **`observed_types.txt`** — 564 polymorphic `$type` discriminators. Objects carry
  `"$type":"HyperQuest.GameServer.Contracts.X, HyperQuest.GameServer.Contracts"`;
  the client selects the subtype from it, so nested/contract objects in a message
  **must** include `$type` — the example generator now emits it.
- **`validation_report.txt`** — cross-check vs the reversed schemas: field names
  confirmed, and it surfaces **inherited base-class fields the codec walk misses**
  (serialize delegates common fields like `Id`/`Points`/`DescriptionId` to a base
  method), so the game data is the more complete source for those types.

### Enum values & required/optional (codec investigation — see above for the data)
- **Enum value = a 64-bit name hash.** The reader (`009a8670`) accepts either
  `"0x"+16 hex` (parsed as the raw value, `FUN_00401670`) or a **name string**
  which it **hashes** (`FUN_009ce4b0`, a CRC-style 64-bit hash over tables
  `DAT_01061250`/`DAT_01060a50`). So the wire accepts `"0x...."` or the member
  name (e.g. `"AttackType_Normal"`); the parse never range-checks, so any value is
  *well-formed*. The set of *valid* members is game-design data (names, one-way
  hashed) — it is **not** in the generic codec, so there is no value table to
  extract here. Safe default: `"0x0000000000000000"`.
- **Required vs optional is not marked.** Deserialization is key-driven: a missing
  key leaves the constructor default (0 / "" / false). There is no "missing
  required field" check in the codec. The robust rule for the server is therefore
  **emit every field** (the generated examples already do), so nothing is ever
  missing; when reading client requests, tolerate absent fields (use defaults).

**Authority:** the *serialize* side is the reliable source of a field's shape
(its object/array writers are unambiguous), so the generator prefers it. The
*deserialize* walker is noisier — its dispatch loop reads the incoming JSON *key*
via a string primitive, which a static walker can misattribute as a field value
(verified on `ShopFilterValueId`: two ints, mis-seen as a string). So the
`validate_consistency.py` "type" diffs are mostly deserialize-walker artifacts,
not real protocol conflicts; the dynamic round-trip (`autovalidate.py`, which
*runs* the real code) is the ground truth.

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
out through the real serialize. Over the **395 two-way all-scalar contracts**:
- **INCOMING: 356 / 395 (90%)** have *every* field parsed correctly by the
  client's real reader (int/number/bool/string/datetime);
- **full round-trip (both directions): 336 / 395** — the rest are contracts whose
  only fields are floats/numbers the serialize emits through writers we don't
  capture (incoming still validated), plus a few reader types not yet fed.

See `re/catalog/network/roundtrip_report.txt`. Contracts with nested-object
fields are covered by the static consistency check above. (Key harness detail:
the codec's char-advance and writer primitives are `stdcall`, so the intercept
layer pops their callee args — `emu.py` `intercept_cleanup`.)

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
