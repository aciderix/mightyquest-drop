# Game systems — architecture of the gameplay code

Reconstructed from the ~4,800 source files the build left in assert/log strings
(`re/catalog/subsystems/`). This is the hand-written game logic, independent of
the renderer and the third-party libraries.

## Module overview
| Module | Files | What it is |
|--------|------:|------------|
| `GameServerProxies` | 4,484 | Generated RPC proxies + JSON serializers (the protocol). See `01-SERVER-API.md`. |
| `Simulation` | 161 | The deterministic gameplay simulation — combat, creatures, buildings, AI. |
| `Gameplay` | 90 | Meta-game scripting: objectives, achievements, scripted level actions, UI controllers. |
| `Engine` (Zouna) | 91 | Engine services used by the game (containers, file mgr, input, render, JSON). |
| `BehaviorTree` | 8 | Generic behavior-tree node types driving creature AI. |
| `LibPC` | 11 | Zouna PC platform layer. |

## Simulation — an Entity/Component/System (ECS)
Entities are composed of `*Component`s; behaviour is driven by behavior-tree
`Action*` / `Condition*` / `Decorator*` nodes. Notable pieces (file list in
`re/catalog/subsystems/Simulation_files.txt`):

- **Stats / life**: `CreatureStatsComponent`, `BasicLevelingComponent`,
  `CreatureTiersComponent`, `CreatureBoostComponent`, `DamageDealerComponent`,
  `DestructibleComponent`, `DestructibleBuildingComponent`, `CorpseComponent`.
- **Abilities / buffs**: `AbilityManagerComponent`, `BuffableComponent`,
  `BuffCreatorComponent`, `*BuffEffect` (Confusion, DamageModifier, …),
  `AuraCarrierComponent`.
- **AI**: `AiControllerComponent`, `CreatureAiComponent`, `AggroComponent`,
  and BT actions `ActionAggro/MoveTo/UseAbility/Fear/Wander/Leash/Idle/…`.
- **Targeting conditions**: `ConditionTarget*` (Exists, Is, WithinDistance,
  IsAggroed, LevelIs, …), `ConditionHealthIsLessThan`, `ConditionIsAbilityCastable`.
- **Area effects / projectiles**: `CircleFieldComponent`, `BeamFieldComponent`,
  `ChainComponent`, `BallisticMove`, `BallisticAutoPitchMove`, `AimedCannonComponent`.

**Determinism.** `Gameplay\DeterminismTestGame` plus the strictly data-driven
component model indicate the simulation is **deterministic** (same inputs →
same outcome). This is why the game can record/replay attacks and why a server
can validate a battle outcome without rendering it — directly relevant to a
community server (anti-cheat + replays).

## Gameplay — scripted meta-game
Two big families (file list in `re/catalog/subsystems/Gameplay_files.txt`):
- **`*AssignmentAction`** — scripted level steps the game can trigger:
  `LaunchAttackAssignmentAction`, `GenerateProceduralCastleAssignmentAction`,
  `AddItemsToInventoryAssignmentAction`, camera/UI/sound actions, etc.
- **`*ObjectiveConditionChecker` / `*AchievementChecker`** — win/quest/achievement
  evaluation: `DefeatCastleObjectiveChecker`, `KillEntitiesObjectiveChecker`,
  `NoHeroDeathObjectiveConditionChecker`, `HeroReachLevelAchievementChecker`, …
- Game-loop entry points: `MyGame`, `Controller`, `HQStats`.

## Where to dig next (each is a tractable workstream)
1. **Combat formulas** — reverse `CreatureStatsComponent` / `DamageDealerComponent`
   / `BasicDamageModifier` to recover damage/leveling math (server needs it).
2. **Ability/buff system** — `AbilityManagerComponent` + `*BuffEffect`.
3. **Castle/building** — `DestructibleBuildingComponent`, build validation in Gameplay.
4. **AI** — the BT node set + `ActionUseAbility` targeting.
5. **Determinism/replay** — `DeterminismTestGame`, needed for server-side validation.

Pair static reading (Ghidra, using the 5,951 source-anchored functions) with
Unicorn micro-emulation (`emu.py`) to verify formulas on concrete inputs.
