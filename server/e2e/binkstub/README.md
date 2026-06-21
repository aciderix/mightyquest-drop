# bink2w32 stub — skip the intro movie under Wine

The client plays an intro Bink movie (`PlayMovie DB:>Movie>Ubisoft_Logo.bk2`)
during boot. Under headless Wine the real `bink2w32.dll` path stalls the boot.

This stub DLL exports the same 83 symbols as the real `Bin/bink2w32.dll`
(matching names + ordinals so the game's IAT resolves), but `BinkOpen` returns
NULL and `BinkShouldSkip` returns 1 — so the engine treats the movie as "failed
to open" and **skips it gracefully**. Confirmed: with `winver=win7` + this stub,
the client boots past `LoadGameSettings` and past the intro movie
(`WaitPlayingMovieEnd`) into font/UI init.

## Build (32-bit MinGW)
    i686-w64-mingw32-gcc -shared -O2 -o bink2w32.dll stub.c bink.def -static-libgcc

`stub.c` / `bink.def` are generated from the real DLL's export table; regenerate
if the game build changes. See `../LIVE_CLIENT.md` for the full launch recipe
(winver=win7 fix) that precedes this step.

## Deploy
    cp Bin/bink2w32.dll Bin/bink2w32.dll.orig     # back up the real one
    cp bink2w32.dll Bin/bink2w32.dll
    # launch with WINEDLLOVERRIDES="winhttp=n,b;bink2w32=n"

## Status
Gets past the intro. The next boot wall is a separate Wine/no-GPU null-deref at
`0x009CA2AF` during `InitFonts` (a UI table at `this+0x80` is null) — NOT a data
problem: all 51 bigfiles are present and real (893 MB, 0 LFS pointers).
