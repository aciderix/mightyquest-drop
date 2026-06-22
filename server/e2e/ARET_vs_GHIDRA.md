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
