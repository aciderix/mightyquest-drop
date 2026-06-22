# Complete in-container test of the game ("test complet")

## What it exercises (and what it can't)
A full run wires the three real pieces together:
1. `start_stateful_server.sh` — the self-hostable catalog server on TLS :443
   (gate-complete responses, enum integers, stateful, envelope).
2. `launch_lobby.sh` — the real client under Wine (DXVK, bink stub patches,
   `--remote-debugging-port`), pointed at `https://127.0.0.1`.
3. `cdp/agent.py` — drives the hyperquest flow and validates every response.

This validates, end to end and headless: **boot → DXVK render init → TLS connect
→ HTTP 200 on the API → time-sync → response parsing by the client**. It is a
real correctness test of the server against the actual game binary.

A *visual, interactive* playthrough is NOT possible in this container: the
embedded Chromium-28 renderer doesn't run page JS under headless software Wine
(documented in LIVE_CLIENT.md §4-5). That needs a real Windows/GPU host; there
the same server + agent drive the real UI.

## What the complete test FOUND (this is its value)
Running it surfaced a bug class invisible to the schema gate alone: **list fields
the catalog mistyped as `object` are emitted as `{}`, and the client's native JSON
parser aborts** — `JSON ERROR: Memory Stream(1,N): Expected character: '['` →
`OpenOpalPanel : ErrorPanel`, immediately after a *successful* 200 on
`GetAccountInformation`. The wire/JSON shape was wrong even though every field was
present and enum-correct. This is exactly the "fields received but wrong reaction"
class.

Fixes applied: the gate now emits `[]` for known list fields
(`array_fields.json`: schema arrays + example-unanimous arrays + the
game-confirmed `CreatureArchetypes`). With those, the client parses past the first
errors.

## Honest limit of the automated fix
An automated "game-oracle loop" (launch → read the parser's error offset → mark
that field as a list → relaunch) closed ~10 more fields but then became
unreliable: the client's byte offset doesn't map cleanly to our response when
empty fields cluster, so it began over-correcting (flipping a real object to
`[]`, which then errors `Expected '{'`). Precise per-field list-vs-object typing
needs a more reliable source than offset-matching — the binary's array *writer*
(what the client itself serializes as an array) or the contract RTTI shapes. That
is a bounded RE pass, listed as the next step.

## Net
The complete test is **possible and valuable**: it boots the real game, connects
to the self-hostable server over TLS, and validates response correctness against
the actual client — catching real shape bugs the offline gate can't. The flow
contracts are clean; the remaining work is precise list/object typing for the UI
models, and a real-GPU host for the visual layer.
