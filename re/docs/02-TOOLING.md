# Tooling — what we use, and specifically what Unicorn is for

## The toolkit (in `re/tools/`)
| Tool         | Purpose | Needs |
|--------------|---------|-------|
| `analyze.py` | PE layout, module split, source-tree, server contracts/controllers | pefile |
| `rtti.py`    | C++ class catalog + vtables from MSVC RTTI | pefile |
| `emu.py`     | Unicorn micro-emulation harness (run one routine) | pefile, unicorn |
| `re/ghidra/ExportAndLabel.java` | Ghidra post-script: label functions from source-path strings + export `functions.csv` | Ghidra |

Install once: `pip install pefile capstone unicorn`.

## Ghidra (static disassembly / decompilation)
Ghidra 12.x runs headless against the client:
```bash
ghidra_*/support/analyzeHeadless <proj_dir> MQ \
  -import mq_client.exe \
  -scriptPath re/ghidra -postScript ExportAndLabel.java re/catalog/functions.csv
```
This is the heavy lifter: it disassembles the ~10 MB `.text`, recovers functions,
and (via the post-script) reuses the build's leftover source paths to label many
functions with their originating `.cpp`. Expect a long first run.

**Known issue — broken IAT.** The unpacked dump only resolved one import per DLL,
so calls through the import table land on garbage. Two consequences:
- Some "function contains referring thunk" / decompile warnings are expected.
- Cross-references to OS/library functions are mostly absent until the IAT is
  rebuilt (Phase 1). Rebuilding it (e.g. Scylla-style, or by matching call sites
  to the `.UBX1` import table) is the main thing that improves decompilation
  quality across the board.

## What Unicorn is — and is NOT — for here
Unicorn emulates a **CPU only**: no Windows, no DLLs, no GPU, no heap, no syscalls.
You **cannot boot the game** with it, and that was never the right use.

Its job in this project is **micro-emulation**: take one *isolated* routine that
Ghidra located, give it inputs in registers/memory, run it, and read the output.
That turns "I think this function does X" into a verified fact without a Windows
machine. The harness (`emu.py`) maps the PE at its real addresses, sets up a
stack, and **stubs every call that leaves `.text`** so leaf-ish routines complete.

Good targets (self-contained, little/no OS interaction):
- **Serializers** — run a `*Serializer` routine on a sample struct and capture the
  exact JSON bytes it emits → nails down the wire format for the community server.
- **Hashing / checksums** — confirm the algorithm used for asset IDs, save
  integrity, or request signing.
- **Token / signature derivation** — reproduce how a session token or request
  signature is computed from inputs (key part of faking the login handshake).
- **Small decoders** — e.g. a routine that decodes a config blob.

Poor targets: anything with a deep call graph into curl/OpenSSL/heap/OS — stubbing
those out changes behaviour. For those, prefer Ghidra reading + a live capture.

### Typical workflow
1. Ghidra: find the function VA + prototype (args, calling convention).
2. `emu.py`: `Emu(exe).call(va, [args], ecx=this_ptr)`; pre-load input buffers
   with `write()`, read results with `read()`.
3. Compare output against a hypothesis (JSON shape, hash value, token).
4. If a specific external call must return a real value, set `emu.stub_rets[va]`.

This pairs with Phase 2 of the roadmap: reverse a serializer statically in
Ghidra, then *prove* the wire format by emulating it in Unicorn.
