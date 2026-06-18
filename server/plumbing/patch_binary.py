#!/usr/bin/env python3
"""
MQEL Binary Patcher
====================
Patches the unpacked MightyQuest.exe to fix SSL certificate loading on Windows.

Problem:
  The game's statically-linked libcurl 7.38.0 + OpenSSL was compiled with
  OPENSSLDIR=/usr/local/ssl. On Windows this path doesn't exist, so
  SSL_CTX_load_verify_locations(ctx, "/usr/local/ssl/cert.pem", NULL) fails,
  leaving an empty trust store. Any server certificate is then rejected with
  "SSL certificate problem: unable to get local issuer certificate".

Fix:
  Replace the compiled-in path "/usr/local/ssl/cert.pem" (22 bytes) with
  "ca.pem" (6 bytes, null-padded to 22). The launcher deploys our CA cert
  as "ca.pem" next to MightyQuest.exe, and launches the game with that
  directory as the working directory — so the relative path resolves correctly.

Usage:
  python patch_binary.py [unpacked_exe] [output_exe]

  Default unpacked_exe: ReverseEngineering/Executable/MightyQuest_unpacked_fixed.exe
  Default output_exe:   server/MightyQuest_mqel.exe
"""

import os
import sys

# Exactly 22 bytes (the length of "/usr/local/ssl/cert.pem")
OLD_PATH = b'/usr/local/ssl/cert.pem'
NEW_PATH = b'ca.pem'

assert len(OLD_PATH) == 23, "sanity check"
assert len(NEW_PATH) <= len(OLD_PATH), "new path must fit in old slot"

# Null-pad new path to same length as old (so binary layout is unchanged)
NEW_PATH_PADDED = NEW_PATH + b'\x00' * (len(OLD_PATH) - len(NEW_PATH))


def patch(src, dst):
    print(f"Reading {src} ...")
    with open(src, 'rb') as f:
        data = bytearray(f.read())

    # Find all occurrences
    idx = 0
    patched = 0
    while True:
        pos = data.find(OLD_PATH, idx)
        if pos == -1:
            break
        data[pos:pos + len(OLD_PATH)] = NEW_PATH_PADDED
        print(f"  Patched at file offset 0x{pos:08X}")
        patched += 1
        idx = pos + len(NEW_PATH_PADDED)

    if patched == 0:
        print(f"ERROR: Pattern '{OLD_PATH.decode()}' not found in {src}")
        print("       Make sure you're using the UNPACKED exe, not the original packed one.")
        sys.exit(1)

    print(f"Writing {dst} ...")
    with open(dst, 'wb') as f:
        f.write(data)

    print(f"Done — patched {patched} occurrence(s).")
    print()
    print("Next steps:")
    print("  1. python server/launcher.py")
    print("     (The launcher will deploy this patched exe automatically.)")
    print("  OR manually:")
    print(f"  2. Copy {dst} to GameData\\Bin\\MightyQuest.exe")
    print("  3. Deploy your CA cert as GameData\\Bin\\ca.pem")


def find_unpacked_exe():
    """Find the unpacked exe relative to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "..", "ReverseEngineering", "Executable", "MightyQuest_unpacked_fixed.exe"),
        os.path.join(here, "MightyQuest_unpacked_fixed.exe"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return os.path.normpath(c)
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) >= 2:
        src = sys.argv[1]
    else:
        src = find_unpacked_exe()
        if not src:
            print("ERROR: Could not find MightyQuest_unpacked_fixed.exe")
            print("       Pass the path as the first argument:")
            print("       python patch_binary.py <unpacked_exe> [output_exe]")
            sys.exit(1)

    if len(sys.argv) >= 3:
        dst = sys.argv[2]
    else:
        dst = os.path.join(here, "MightyQuest_mqel.exe")

    if not os.path.isfile(src):
        print(f"ERROR: File not found: {src}")
        sys.exit(1)

    patch(src, dst)


if __name__ == "__main__":
    main()
