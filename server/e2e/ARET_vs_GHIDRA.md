# Validating uncertain enum integers — ARET vs Ghidra vs self-labeling

The server-only enums (not in the client JS) can't be guessed by byte/pattern
scans (we measured: .rdata-offset 22/65, getter-order 49/65, +0x17 byte 84 %,
dispatch-table 38/65 — all unreliable). The reliable source is each enum's
`*_FromString` parser in the binary: a `strcmp` cascade with the **explicit
value literal** per member. Both decompilers read it cleanly.

## Method
Each enum has `EnumFromString(char* s, int* out)`:
`if(strcmp(s,"Member")==0){ *out = <VALUE>; return 1; }` per member.
Point the decompiler at that function; read `<VALUE>` next to each member.

## Head-to-head (same functions)

| Function | self-labeling / client-JS truth | ARET | Ghidra 12.1.2 |
|---|---|---|---|
| `CastleRenovationLevel` @0x520CF0 | RenovationComplete=5 (levels 0-4) | **5** ✓ | **5** ✓ |
| `AttackSource` @0x708010 | client JS: Regular=0 … Chat=6 … Guild=9 | **100 % match** ✓ | (consistent) |
| `CreatureRank` @0x4D3CF0 | flags | None=0,Grunt=1,Captain=2,Elite=4,**Boss=8**,All=-1 ✓ | **identical** ✓ |
| `NotificationType` @0x6BA0E0 (99 members) | — | CastleBought=86, WalletUpdated=24, FriendshipInvite=1 | **identical** ✓ |

**ARET and Ghidra produced identical enum values on every function tested, and
both matched self-labeling / the client-JS ground truth.**

## Verdict — is ARET reliable, and how does it compare?
- **Correctness: equal.** On these `FromString` cascades ARET == Ghidra == truth.
  ARET's recent fixes (tail-call esp, lea-segment) lift this control flow cleanly.
- **ARET pros:** self-contained Rust binary, fast per-function (`aret bin
  --function <hex>`, no project/analysis step), lifted the whole image (54925
  functions), and **annotates string args inline** (`/* "RenovationLevel0" */`).
  Output is nested `if/else`.
- **Ghidra pros:** more battle-tested generally; flat `if + early return` output is
  marginally easier to parse; resolves strings as real literals. Cost: ~570 MB +
  Java, and a slow first-pass auto-analysis (minutes) before scripting.
- **The actual hard part is FUNCTION SELECTION** (which `FromString` belongs to a
  given contract field), not the decompilation — automated selection mis-picks
  flags/variant functions, so we hand-verify the address per enum. Both tools are
  equally affected by this; it's not a decompiler weakness.

## Applied (dual-confirmed → confirmed_enums.json)
`NotificationType`, `CreatureRank`/`Rank`, `CastleRenovationLevel` family — all
ARET∩Ghidra identical. self-check as-emitted rose 1078 → **1182/1307**;
`GetAccountInformation` is now fully schema-clean.

`EntityType.Ability=10` was also dual-extracted but **not** applied: its contract
field is the generic name `"Type"`, and the gate matches enums by field name, so
auto-mapping `Type` risks collisions with other contracts' `Type` fields. It
stays flagged in `uncertain.log` rather than risk a wrong conversion.

## Why bulk auto-resolution of the remaining ~140 is NOT safe (measured)

The tempting shortcut — extract every `FromString` cascade in the binary and
auto-convert by value — was tested and **rejected**:

- Full ARET lift (54925 funcs) parsed → catalog; an "all cascades agree on the
  value" rule **contradicted the client-JS ground truth in 18 cases**.
- Re-built from **Ghidra's flat output** (unambiguous name↔value pairing, not a
  parsing artifact) → still **15 contradictions** vs client-JS, e.g.
  `ControllerNames.attack` JS=9 / binary=10, `RewardItemType.CraftingMaterials`
  JS=10 / binary=49, `AchievementType.DefeatCastle` JS=1 / binary=8.

These are **genuine divergences**: the client has more than one enum value
system (the JS-UI enums vs the native/wire enums), and member names are reused
across enums with different integers. So no value-only or name-only rule can be
trusted — auto-converting would re-introduce the silent-default bug it aims to fix.

### The clean & safe procedure (what we actually do)
1. **Scope by `Contract.Field`** in `confirmed_enums.json` (gate pillar 1) — no
   field-name collisions, so even a generic `Type` field can be fixed per contract.
2. **Per enum, confirm from the binary** by decompiling the *specific* parser/
   deserializer with **both ARET and Ghidra**; accept the mapping **only if the two
   tools agree** (and it matches any overlapping client-JS / self-labeling truth).
3. **Convert only what is confirmed this way; never guess.** Everything else stays
   in `uncertain.log` with the exact `Contract.field=value`, so an in-game glitch
   is traced to the suspect field in seconds.

Confirmed so far (dual-tool): the client-JS 65 + NotificationType, CreatureRank/
Rank, CastleRenovationLevel family → as-emitted 1078→1182/1307. The remaining
~140 are flagged, not guessed. They are closed the same way, one verified
`Contract.Field` at a time, when a given flow needs them.
