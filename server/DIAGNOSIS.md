# DIAGNOSIS — symptôme in-game → signature trace → où corriger

Procédure : `python diagnose.py` (puis `--grep <Service>` / `--method <X>` /
`--tail 40`). Chaque ligne de `trace.jsonl` a une `source` et des `flags`.
Détail du pipeline : `AI_GUIDE.md`.

| Symptôme en jeu | Signature dans la trace | Cause / où corriger |
|---|---|---|
| Un écran/onglet est **vide ou inerte** | `source=fallback_example` sur ce service | pas de handler dédié → données statiques. Câbler dans `stub_server.ep_social` ou `ENDPOINTS`. |
| **Achat** sans effet (or non déduit / pas d'objet) | `method=SendCommands`, commande `Buy*` | `command_notifications._apply` (Buy*) ; prix via `catalog_economy.sku_price`. |
| **Équipement** refusé / pas d'effet | `flags: command_rejected:HeroEquipmentEquipCommand` | `catalog_economy.can_equip` a refusé (slot↔catégorie ou niveau). Vérifier l'objet/slot. |
| Objet équipé **sans bonus de stats** | équip OK mais `HeroStatModifier` vide | `catalog_economy.hero_equipped_stats` / l'objet n'a pas de `MagicalProperties` (qualité Basic). |
| **Construction** : créature/piège non posé | `SendCommands` `AddCastleCreature/Trap` | `_apply` ; coût via `creature_cp/trap_cp` ; cap `castleheart_max`. |
| **Loot** absent / pas enregistré | `method=EndAttack` | `stub_server.ep_end_attack` ; loot = Σ créatures (`castle_rewards`). |
| **Quitter le combat** casse l'écran | `EndAttack`, `CompletionType` | doit renvoyer un `EndAttackInfo` complet (jamais `{}`). |
| **Or/xp/trophées** d'un montant douteux | `EndAttack` / PvP | économie catalogue (`catalog_economy`) ; 2 valeurs dérivées : force-vitale/kill, perte trophée. |
| **Créatures niveau aberrant / combat 3D** plante | pas de requête fautive en trace | **moteur natif** (hors serveur). Vérifier que `StartAttack` renvoie `CreatureTiers` non vide (`e2e/cdp/combat_inspect.py`). |
| Client **plante** sur une réponse | `flags: exception` ou réponse incomplète | voir l'enregistrement `error`/`traceback` ; vérifier la complétude (`completeness_gate`). |
| Connexion **refusée** au lancement | aucune requête n'arrive | TLS : CA non fiable ou bundle curl (voir `windows/README.md` § TLS). |

Règle anti-hallucination : si la trace **ne contient pas** la requête correspondant
au symptôme, ne pas inventer une cause serveur — c'est probablement côté
client/combat 3D/TLS. Le dire explicitement.
