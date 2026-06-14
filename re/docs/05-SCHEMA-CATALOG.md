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

## Caveats / next refinements
- Field **types** aren't captured yet (only names + order). Types can be added by
  reading each method's writer-primitive calls (writeInt/writeString/writeArray/
  writeObject) — a follow-up pass on the same methods.
- A few stubs (~150) had no fields recovered (empty/marker contracts or unusual
  vtable shapes); revisit if needed.
- Nested object/array fields are listed by key; the referenced child contract can
  be linked by matching field name → contract name.
