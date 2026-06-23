# AI_GUIDE — comprends ce pipeline sans contexte préalable

Tu es une IA qui doit aider sur ce serveur. Lis ce fichier en entier : il explique
le pipeline, comment diagnostiquer un bug in-game, et comment étendre, **sans
supposer aucun contexte**. Complément : `SERVER.md` (architecture/limites),
`DIAGNOSIS.md` (symptôme→cause), `windows/README.md` (test sur PC).

## 1. Ce que c'est
Un **backend self-hosté** de *The Mighty Quest for Epic Loot* (jeu Ubisoft 2014,
serveurs morts). Le client parle à `gs.themightyquest.com` en HTTPS ; on le pointe
sur ce serveur local. Le serveur sert le **vrai contenu** du jeu (catalogue
déchiffré) et tient l'état (compte, héros, château, social, économie).

Principe directeur : le client a un **désérialiseur silencieux** — un champ
manquant/mal typé est remis à 0/""/{} **sans erreur**, ce qui casse le gameplay
discrètement (créatures niveau 4 milliards, loot fantôme, barre de skills vide…).
Donc **chaque réponse doit être schéma-complète et correctement typée**. C'est le
rôle de la *gate*.

## 2. Le pipeline de données (de la requête à la réponse)
```
client (HTTPS /<Service>Service.hqs/<Method>)
  -> stub_server.Handler._handle           routage
     -> ENDPOINTS[method]   (handler dédié, ex. ep_start_attack)        \
        ou ep_social(...)   (guilde/ami/news/shop/classement/journal)    } produit un contrat
        ou _guess(method)   (FALLBACK: exemple statique, schéma-complet) /
     -> contract(name, **overrides)         completeness_gate.complete()  remplit + enums->int
     -> envelope(...)        {"Result":...} ou {"Notifications":[...]}
  -> debuglog.trace(...)     une ligne JSON dans trace.jsonl (source + flags)
  -> réponse au client
```
Les **mutations** (achats, équip, construction, progression, social) passent par
`SendCommands` → `command_notifications.CommandBus.handle` → `_apply` (mute l'état
+ émet les vraies notifications). Les valeurs d'**économie** (loot, prix, stats,
trophées) viennent de `catalog_economy` (formules du catalogue).

## 3. Les modules (rôle en une ligne)
| Fichier | Rôle |
|---|---|
| `stub_server.py` | serveur HTTP/TLS, routage, handlers d'endpoints, état (`State`) |
| `completeness_gate.py` | rend chaque réponse schéma-complète, enums→entiers (anti silent-default) |
| `gameplay_catalog.py` | indexe le catalogue déchiffré (`catalog/GameplaySettings`, 2538 entrées) |
| `catalog_economy.py` | formules réelles : vente, drop/qualité, stats d'objets, mine, trophées, `can_equip` |
| `command_notifications.py` | bus `SendCommands` stateful (43 commandes) + audit |
| `debuglog.py` | trace structurée JSONL (`trace.jsonl`) |
| `diagnose.py` | lit la trace → rapport de diagnostic pour IA |

## 4. Concept clé : `SpecContainerId` = id de dossier de catégorie (par CONTEXTE)
Les ids ne sont **pas** un registre global unique (collisions entre catégories).
Le champ donne la catégorie : `CreatureTiers[].SpecContainerId`→`Creatures`,
`TrapTiers[].SpecContainerId`→`Traps`, `Room.SpecContainerId`→`Rooms`. Ex.
créature 1081 = `Creatures/001081 - Chicken`. D'où loot/xp/coût par créature réels.

## 5. Diagnostiquer un bug in-game (procédure)
L'utilisateur dit « j'ai fait X, il s'est passé Y ». Toi :
1. `python diagnose.py` → erreurs, fallbacks, commandes rejetées (chacun pointe le
   fichier/handler).
2. cible : `python diagnose.py --grep <Service>` ou `--method <X>` ou `--tail 40`.
3. interprète les **flags** de `trace.jsonl` :
   - `fallback_example` → pas de handler dédié → réponse **statique/inerte** (cause
     n°1 d'un écran vide). Fix : ajouter un handler dans `ENDPOINTS` ou `ep_social`.
   - `command_rejected:<Cmd>` → mutation refusée (ex. `can_equip` slot/niveau). Voir
     `command_notifications._apply` + `catalog_economy`.
   - `command_unknown/heuristic:<Cmd>` → edge notif non confirmé.
   - `exception` → un handler a levé ; voir l'enregistrement `error`/`traceback`.
4. ne **suppose rien** hors de la trace : si la trace ne montre pas la requête,
   c'est probablement **côté client/combat 3D** (hors serveur), dis-le.

Anti-hallucination : chaque réponse du serveur est traçée avec sa **source**. Si
tu ne sais pas pourquoi une valeur est « bizarre », `grep` l'`ExpirableId`/le
`method`/le champ dans `trace.jsonl` et `uncertain.log` avant de conclure.

## 6. Étendre (recettes courantes)
- **Rendre un service vivant** (sort de `fallback_example`) : ajoute un cas dans
  `ep_social` (ou un handler `ENDPOINTS`) qui lit/mute l'état et renvoie le contrat.
- **Câbler une commande** : ajoute un cas dans `CommandBus._apply` (mute `acc`,
  renvoie des notifications via `self.build`) et liste-la dans `STATEFUL`.
- **Sourcer une valeur du catalogue** : ajoute un accès dans `catalog_economy.py`
  (lis `GameplaySettings/<Catégorie>/...` via `gameplay_catalog`).
- **Toujours** : passe la réponse par `contract(name, ...)` et pose les vraies
  listes/objets **après** la gate (sinon elle peut les écraser).
- **Vérifie** : `python e2e/full_game_test.py` (doit rester vert).

## 7. Limites honnêtes (ne pas chercher un bug serveur là où il n'y en a pas)
- **Combat 3D** : simulé par le moteur natif du client (pas le serveur). Le serveur
  fournit château+héros et réconcilie le loot à `EndAttack`. Un crash de combat 3D
  = client/GPU, pas serveur.
- **2 valeurs dérivées** (absentes du catalogue) : force-vitale par kill, perte de
  trophées du défenseur.
- **Services temps-réel** (chat/replay/événements live) : `fallback_example`.
- **Edges notif** : forme exacte, ordre/type non confirmés octet-par-octet
  (auto-réparés par relecture de `GetAccountInformation`).

## 8. Lancer / tester
```bash
# Linux/dev
python3 stub_server.py --host 127.0.0.1 --port 443 --tls [--debug]
python3 e2e/full_game_test.py        # 54 checks réseau
python3 diagnose.py                  # diagnostic depuis trace.jsonl
# Windows (vrai jeu) : voir windows/README.md (setup.bat puis run.bat)
```
Variables : `MQ_TRACE` (chemin trace), `MQ_DEBUG=1` (echo), `MQ_CATALOG` (chemin
catalogue). État dans `state.json` (supprimer = repartir de zéro).
