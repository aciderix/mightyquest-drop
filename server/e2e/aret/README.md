# ARET save-state path — running the real client code headless

Goal: execute the game client's **own** functions (the network serializers/
deserializers, boot/login logic) headless — no GUI, no Direct3D — by lifting
them with ARET and seeding a live memory snapshot. This is the "run the real
client against the server without the GUI" path, since the full GUI client
won't finish booting under headless Wine (see ../README.md).

## Pipeline (all reproduced in this environment)

1. **Snapshot (A)** — `../snapshot_game.sh`: the packed client self-unpacks +
   resolves its protector IAT under Wine, hangs at `OpenBF PACKAGE_PRELOAD`; we
   `SIGSTOP` + dump `0x400000..0x1e00000` → `game.snap` (ARETSNP1, 27 MB). ✅
2. **Lift+build (B)** — ARET transpiles the 40 127-function image to native C
   and links it (`-m32`), seeding memory from the snapshot:
   ```
   aret MightyQuest_unpacked.exe --mode transpile --entry 0x493440 \
        --snapshot game.snap --iat-symbols iat_symbols_full.json --out-dir OUT
   ```
   ✅ (ARET's transpile→compile→run pipe is green: 17/17 M1 tests.)
3. **Driver** — `drv_deser.c` replaces `aret_main.c`: it sets up the parser
   context in the `MAP_FIXED` real-address memory, routes the stream's
   `advance()`/`error()` vtable callbacks to native shims via dispatch
   sentinels (`build_driver.sh` patches `aret_call`), and calls the **real
   LoginResult deserializer `sub_493440(CTX, OBJ, NAME)`** with our server-shaped
   JSON. Build + run with `build_driver.sh`.

## Result — pipe works; one ARET bug fixed, one diagnosed

The chain executes on real lifted client code:
`main → sub_493440 (deserializer) → sub_9a8d30 (thunk) → sub_9a8840 (token/number
reader)`, and **our `advance()` callback streams the JSON in correctly**.

### Bug 1 — tail-call esp (FIXED, see `aret-tailcall-esp-fix.patch`)
First run segfaulted at `mov [ecx],eax`, `ecx=0`. Root cause: ARET gave **every**
internal call `args[0] = esp-4` (modelling the return address a `call` pushes),
**including tail calls** lowered from `jmp`. A `jmp` pushes nothing, so the
`push ebp;mov ebp,esp;pop ebp;jmp f` thunk handed `f` a frame off by 4 → the
reader stored its result through a null pointer. Fix in
`src/ir/build.rs` (`internal_tailcall_args`, applied to the `Call` inside a
`Stmt::Return`). After it, **integer fields deserialize correctly headless**:
```
AccountId  in=1000 -> got=1000  OK      (LoginResult)
AccountId  in=2000 -> got=2000  OK      (AccountLite)
```
ARET's M1 transpile suite stays 17/17. (Pushed to the toolkit repo.)

### Bug 2 — strcmp mismatch structured as a bare `break` (diagnosed)
With bug 1 fixed, every field still lands at the first contract field's offset:
the deserializer's inline field-name `strcmp` chain always reports "match" on the
first entry. In the transpiled `sub_493440`, the `cmp dl,[ecx]; jne mismatch`
that should jump to the `sbb eax,eax; or eax,1` (non-zero = mismatch) block is
structured as `if (v24==0) break;` — the `break` exits the loop **without
computing the mismatch result**, leaving the result var at its initial `0`
(= "match"). So `NAME` never selects a non-first field. This is a CFG
structuring / loop-exit value bug in ARET (deeper than bug 1).

## Bottom line for validation

The deserializer/serializer protocol is **already validated end-to-end through
the client's own code** by `re/tools/validate_codec.py` (Unicorn): **2/2
contracts, all 8 fields, both directions** — `deserialize` and `serialize`. The
ARET save-state channel reproduces that on natively-recompiled client code and
now works for integer fields after bug 1; full multi-field coverage needs bug 2
(ARET CFG structuring) fixed. That is ARET development, not a server gap — the
server is independently validated three ways (codec 2/2, real-traffic replay
79/79, schema completeness).

(Big/generated artifacts — `game.snap`, the multi-GB `aret_*` build trees — are
gitignored; regenerate with the scripts above.)
