#!/bin/bash
# Build the MQEL WinHTTP proxy DLL (cross-compile from Linux)
#
# Prerequisites:
#   sudo apt install gcc-mingw-w64-i686
#
# Output: winhttp.dll (32-bit Windows DLL)

set -e
cd "$(dirname "$0")"

CC="${CC:-i686-w64-mingw32-gcc}"

if ! command -v "$CC" &>/dev/null; then
    echo "ERROR: $CC not found."
    echo "Install with: sudo apt install gcc-mingw-w64-i686"
    exit 1
fi

echo "Compiling winhttp.dll proxy..."
$CC -shared -o winhttp.dll winhttp.c winhttp.def \
    -lkernel32 -O2 -s \
    -Wl,--enable-stdcall-fixup

echo "Built: $(pwd)/winhttp.dll ($(stat -c%s winhttp.dll) bytes)"
echo ""
echo "Deploy: copy winhttp.dll to GameData/Bin/ next to MightyQuest.exe"
