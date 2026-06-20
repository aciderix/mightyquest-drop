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

## Result — pipe works; one ARET lifting gap blocks the clean pass

Running it, the chain executes on real lifted client code:
`main → sub_493440 (deserializer) → sub_9a8d30 (thunk) → sub_9a8840 (token/number
reader)`, and **our `advance()` callback streams the JSON in correctly** — the
reader parses the value (`eax = 1000` for `AccountId`). 

It then segfaults at `mov [ecx], eax` with `ecx = 0` (null store) **inside
`sub_9a8840`**. Root cause is an **ARET IR-lifting gap on that one primitive**,
not the driver or the approach:
- `aret --function 0x9a8840 --mode decompile` shows `__asm__` fallbacks for the
  `shld ecx,eax,2` / `adc [ebp-4],ecx` chain (the 64-bit `*10` atoi accumulator,
  notably `adc` with a **memory destination**).
- `--mode transpile` (the IR pipeline) emits 0 `__asm__` but still computes a
  null pointer for the result store → a semantic mis-lift of that idiom.
- The same `CTX`/`OBJ`/`NAME` inputs deserialize correctly under the Unicorn
  engine (`re/tools/validate_codec.py`, 2/2 both directions) — so the inputs and
  ABI are right; only ARET's native lift of `sub_9a8840` diverges.
- The deserializer routes **every** field (int and string) through this reader,
  so field selection can't dodge it; `sub_9a8840`'s siblings that *are* clean:
  `READ_STRING 0x9a9450`, serializer `0x49de80`, writers `0x9aad80/0x9ab060/
  0x9ab550` — all 0 asm.

## Exact next step

Fix ARET's lift of the `shld`+`adc [mem],reg` accumulator (model `adc` with a
memory destination into the typed IR so the modeled registers stay connected),
then re-run `build_driver.sh` — the deserializer should write `OBJ+off`
correctly and the driver prints a clean PASS. Alternatively, drive the
**serializer** path (`0x49de80`, all-clean) by overriding the writer symbols
(`objcopy --weaken-symbol` on their chunk `.o` + strong shims) to capture the
emitted key/value wire format.

(Big/generated artifacts — `game.snap`, the multi-GB `aret_*` build trees — are
gitignored; regenerate with the scripts above.)
