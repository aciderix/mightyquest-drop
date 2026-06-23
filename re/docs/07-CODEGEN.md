# Generated types & server options

`re/tools/gen_types.py` turns the reversed schema catalog into neutral,
reusable type definitions — the foundation any community server can build on,
regardless of language.

## Output (`re/catalog/network/generated/`)
- `schemas.schema.json` — one JSON Schema (draft-07), 2,051 contracts under
  `$defs`, each with `x-direction` (request/response/both). Validates as JSON.
- `types.ts` — 2,051 TypeScript interfaces; nested `object` fields are linked to
  their child contract by name (356 links, e.g. `BootConfig.CastleLoadConfig:
  CastleLoadConfig`).

Type mapping: `int/number/float`→number, `string`→string, `bool`→boolean,
`datetime`→string(date-time), `object`→child interface or `unknown`. Regenerate
with `python3 re/tools/gen_types.py`.

## What a "community server" is, concretely
The client only speaks **JSON over HTTP** (plus XMPP for chat). A community
server is just a **program that listens on HTTP** and answers those requests with
the right JSON shapes. The client connects to whatever URL you configure
(`GameServerUrl` / `DistributionServiceUrl`), so:

- **Private / at home**: run the server program on your PC, point the client at
  `localhost` (or your LAN IP), play. Standard "private server" setup for
  abandoned online games.
- **Online**: host the same program on a cheap VPS (or home box with port
  forwarding), give it a public URL, others point their client at it.

Nothing about the server's language has to match the client. Options:

| Option | Pros | Notes |
|--------|------|-------|
| **C# / ASP.NET** | Most faithful — the original backend was C#/.NET (`Contracts.Common.*`). Mature, cross-platform (Linux/Windows), easy hosting. | "ASP.NET" = Microsoft's standard web framework for C#. Best if we want to mirror the original architecture / the 30 controllers 1:1. |
| **Python / FastAPI** | Fastest to prototype a boot→login stub and watch how far the client gets. | Great for the first iteration; can be the long-term server too. |
| **Node / TypeScript** | Reuses `types.ts` directly. | Good DX if you like TS end-to-end. |

The generated types feed all three. Recommended path: a **small stub first**
(boot→login→profile) to prove the client connects, then grow controller by
controller toward the castle/attack loop (ROADMAP phase 3).

## Legal note
Abandoned-game preservation. Keep it non-commercial, ship only our own
reimplementation + these analysis artifacts — never Ubisoft's copyrighted code
or game assets.
