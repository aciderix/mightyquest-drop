# Binary ↔ logs tracer — link the running game's native code to server Q/A

Goal (user's idea): while the game runs, know **which game functions executed at
which moment**, correlated with the server request/response and `MQLog`, and get
that code back as **readable pseudo-C** (the game extracts/runs it naturally, ARET
decompiles it). So for any in-game question — e.g. "where are the mob levels set?" —
we can point at the exact game code.

## Pieces

1. **ARET decompiler** (`aciderix/Automatic-reverse-engineering-toolkit`, branch
   `claude/zen-hamilton-6pi1k4`). Built binary kept at
   `<old-repo>/ReverseEngineering/aret_build/aret.exe` (+ mingw runtime DLLs +
   `winlibs-mingw64.zip` to rebuild). Build needs the Rust **GNU** toolchain
   (`rustup ... --default-host x86_64-pc-windows-gnu`) **and** mingw-w64 on PATH
   (provides `dlltool.exe`, which `windows-sys` needs). Then `cargo build --release`.
   - `aret <unpacked.exe> --mode decompile --split out/`  → 74k `.c` + `index.csv`
   - `aret <unpacked.exe> --function 0x<addr>`            → one function as pseudo-C
   - Run on `ReverseEngineering/Executable/MightyQuest_unpacked_fixed.exe`
     (the in-memory-unpacked exe; the shipped exe is UBX-packed, `.text` raw=0).

2. **`code_sampler.py`** — sampling profiler. Reads every game thread's EIP via
   `SuspendThread` + **`Wow64GetThreadContext`** (the game is 32-bit/WOW64, so a
   64-bit Python MUST use the Wow64 variant — plain `GetThreadContext` returns 0).
   No `DebugActiveProcess` (would risk UBX anti-tamper). ~500k samples in 70s.
   `python code_sampler.py --pid <pid> --seconds 70 --hz 1500 --out s.jsonl`

3. **`trace_link.py`** — maps each sampled EIP → ARET function (the game loads at
   base 0x400000, confirmed: minidump crash VAs match the unpacked exe), filters to
   game `.text` (0x401000..0xDEB000), and windows samples around a server request
   (`--window-after StartAttack`). `aret_index.csv` is the symbol map.

## What it gives / its limit

It reliably shows the **hot functions in a time window** and ties them to the server
timeline (validated: known crash EIPs symbolize correctly; live capture cleanly
separates idle vs combat-load code). Its limit: a **one-shot sub-millisecond**
computation (like assigning ~21 creature levels once at combat load) is often *not
sampled*. Diffing combat-load vs idle narrows to ~112 setup functions, but the level
calc didn't fall in the sample.

## Precise next step for the mob-level computation

Sampling can't catch the brief write; use a **hardware breakpoint**:
1. Game is alive in combat with mobs at level 30 (0x1e). Scan its memory for the
   creature objects (cluster of the tutorial `CreatureTiers` SpecContainerIds
   1,57,56,1081,1028,1057,1029,1003,1001 near a level int) to find the level field
   offset.
2. Set a Dr0 **write** breakpoint on that field (via `Wow64SetThreadContext`,
   Dr7 len=4/RW), become the debugger (`DebugActiveProcess` — accept the anti-tamper
   risk now that the game is already past UBX unpack), catch the write → that EIP is
   the level setter → `aret --function` it.

Behavioral facts to reconcile (mob level): hero **null equipment → mobs lvl 1**;
**complete equipment (ItemLevel 1) → mobs lvl 30 (cap)**; tutorial castle CastleHeart
is **rank 15** (catalog truth) and its creatures are high-tier (invalid at rank 1 →
garbage 1e9). So the level is computed from the attacker's gear and/or the castle's
intrinsic level, NOT from the `AdjustedHeroLevel` we send (it had no effect).
