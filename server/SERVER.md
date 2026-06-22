# MQEL self-hosted server — état, architecture, vérif, limites

Backend self-hosté de *The Mighty Quest for Epic Loot* (édition hors-ligne), stateful,
servant le **vrai contenu** du catalogue déchiffré. Ce document est la trace de
référence (utile si le contexte est compressé).

## Réponse franche : « rien ne manque, tout fonctionne parfaitement » ?

**Non — soyons précis.** Ce qui est **complet et vérifié**, c'est la couche
*serveur* : protocole, contenu réel, état (mutations), réponses schéma-complètes.
Ce qui **n'est pas** « parfait » :

1. **Simulation de combat 3D headless : non exécutable ici.** Le combat tourne dans
   le moteur natif (déclenché par l'UI rendue) ; sous Wine la CEF ne peint pas et
   n'exécute pas le JS de page, et il n'y a pas de GPU. Le *protocole* et le
   *contenu* de combat sont câblés/lisibles, mais faire tourner la sim demande un
   hôte Windows/GPU. (Voir « Combat 3D » plus bas.) **→ seule limite majeure restante.**
2. **Routing commande→notification : forme exacte, edges parfois heuristiques.** La
   *forme* de chaque notification est exacte (schémas) ; le fait que le vrai serveur
   émettait *exactement* ces notifications-là (type/ordre/`NotificationType`) n'est
   pas confirmé octet-par-octet. Impact : transitoire et **auto-réparé** par la
   relecture de `GetAccountInformation` (autoritatif) ; seul l'entier
   `NotificationType` est purement visuel (catégorie d'icône/son).
3. **Quelques montants encore level-scalés faute de mapping.** L'or/force-vitale de
   victoire (50/10 × niveau) et le coût de construction (10) restent des barèmes,
   car le mapping `SpecContainerId → spec créature` n'est pas dans le catalogue
   reversé (donc pas la valeur d'or exacte par créature). **Tout le reste de
   l'économie est sourcé catalogue** (prix de vente, qualité/rareté de drop, stats
   d'objets, courbe d'XP, prix shop).

### Levé depuis la v1 de ce document (désormais réel + vérifié)
- **Économie sourcée catalogue** (`catalog_economy.py`) : prix de vente
  (HEROITEMSELLSETTINGS), qualité/rareté de drop (ATTACKERREWARDSETTINGS +
  EQUIPMENTGENERATIONSETTINGS), **stats d'objets réelles** (MagicalProperties),
  prix shop (ShopSettings). XP déjà sourcé (XpPerLevel).
- **Stats d'équipement réelles** : équiper recalcule `HeroStatModifier` = somme des
  propriétés magiques des objets équipés.
- **Anti-triche loot** : le serveur calcule le butin lui-même (ne fait jamais
  confiance aux montants client) → intrinsèquement plafonné.
- **Services « vivants »** : shop (SKUs réels), classement (trophées), journal de
  défense (PvP enregistré). Reste lecture-seule/exemple : messaging, profil détaillé,
  replay (peu critiques).

Autrement dit : **structurellement complet, économie/stats sourcées catalogue et
vérifiées, services principaux vivants.** Restent : la sim 3D (hôte GPU) et quelques
barèmes faute de mapping créature.

## Vérification (commandes reproductibles)

```bash
cd server
python3 gameplay_catalog.py          # catalogue: 2538 entrées, 0 erreur
python3 command_notifications.py --table   # 43 stateful, 10 no-op, 0 unknown / 53
# serveur + test complet:
python3 stub_server.py --host 127.0.0.1 --port 443 --tls &
python3 e2e/full_game_test.py        # 53/53 checks (réseau, TLS)
```
État au dernier run : catalogue 2538/2538, commandes 0 unknown, jeu **53/53 verts**.

Vérif côté client live (CEF via CDP, nécessite le client lancé, cf. LIVE_CLIENT.md) :
```bash
python3 e2e/cdp/playthrough.py       # onboarding->combat->loot via le framework JS
python3 e2e/cdp/inspect_ui.py        # lit le DOM/texte de l'UI
python3 e2e/cdp/combat_inspect.py    # énumère créatures placées + niveaux
```

## Architecture

```
stub_server.py        serveur HTTP/TLS ; route /<Service>Service.hqs/<Method>
 ├─ gameplay_catalog.py   indexe le catalogue déchiffré (catalog/GameplaySettings)
 ├─ completeness_gate.py  remplit chaque réponse (schéma-complet, enums->entiers)
 ├─ command_notifications.py  bus SendCommands STATEFUL (mute l'état + notifs réelles)
 ├─ catalog_economy.py    formules réelles (vente/drop/stats d'objets/shop) du catalogue
 └─ State (state.json)    comptes, héros, château, social — persistant
```

- **Catalogue** (`catalog/GameplaySettings`, 2538 entrées, 27 catégories) : contenu
  réel — AccountTemplates, Castles (tuto/PvE/BUY), Creatures, HeroTemplates,
  Abilities, Buffs, Traps, Rooms, Oasis (localisation)…
- **Gate** : toute réponse est complétée (aucun champ manquant → pas de
  silent-default), enums convertis en entiers. Les vraies listes (Rooms,
  CreatureTiers, Equipment…) sont posées *après* la gate pour ne pas être écrasées.
- **Command bus** : `SendCommands` mute le compte et renvoie des notifications à
  valeurs réelles (cf. couverture ci-dessous).

## Endpoints câblés (handlers dédiés)

| Service.Method | Rôle |
|---|---|
| Account.GetAccountInformation | état joueur réel (DEFAULTACCOUNT + wallet/héros/château/social) |
| Account.ChooseDisplayName | pseudo (persistant) |
| Hero.ChooseFirstHero | crée le héros depuis HeroTemplate (loadout réel) |
| AttackSelection.GetAttackSelectionList | roster PvE réel par niveau (92 châteaux) |
| AttackSelection.GetCastleInfo | info château réel |
| Attack.StartAttack | PvE (château catalogue) **ou PvP** (château publié d'un joueur) |
| Attack.EndAttack | EndAttackInfo (victoire/escape) + loot scripté + XP héros |
| CastleForSale.GetCastlesForSale | châteaux BUY_* réels |
| ServerCommand.SendCommands | bus stateful (43 commandes) |
| Friendship/Guild/News.* | services sociaux stateful (ep_social) |
| *(autres)* | exemple schéma-complet (fallback sûr) |

## Couverture commandes (SendCommands)

43 **stateful** (mutent l'état), 10 **no-op** délibérés (tracking/idle/*viewed/set*),
0 unknown. Domaines : économie (buy/sell/buyback), forge/crafting, mines, équipement
(gear + spells + consommables), inventaire (move/swap), consommables (activate/expire),
inbox, construction château (créatures/pièges/triggers/buildables), inventaire château,
progression (assignment/select hero), avatar, harvest corpse.

## Modèle d'état (par compte, dans state.json)

```
AccountId, DisplayName, AvatarId, Privileges
wallet {InGameCoin, LifeForce, PremiumCash, ...}
items[]            inventaire (objets lootés/achetés/forgés)
heroes[]           héros (Equipment, EquippedSpells, EquippedConsumables, Level, XP)
selected_hero
castle {Level, CastleHeartRank, creatures[], traps[], triggers[],
        construction_used/max, published}
completed_assignments[]
friends[], guild, guild_invitations[], inbox[], messages[]   (social)
mines {produced, rank}, forge, active_consumables[]
current_attack     château en cours d'attaque (pour le loot d'EndAttack)
```

## Bugs historiques → résolus (mapping)

| Bug vécu (ancien serveur) | Cause | Résolu par |
|---|---|---|
| Créatures niveau 1 milliard | CreatureTiers vide → underflow uint | vrais CreatureTiers du catalogue |
| Loot ne tombe/s'enregistre pas | notifs/loot manquants | EndAttack + bus stateful (item persisté) |
| Barre de skills vide / mauvais slots | Hero.EquippedSpells vide | loadout HeroTemplate + HeroEquipSpell stateful |
| Inventaire non persisté | état non muté | items[] persistant, bus stateful |
| Quitter combat casse l'état | EndAttack renvoyait {} | EndAttackInfo complet (CompletionType) |
| Démarrage non structuré | pas d'état/ordre | DEFAULTACCOUNT + ordre vérifié |

## Combat 3D (la limite restante)

Le combat est **simulé côté client** (déterministe : `AttackRandomSeed` +
`SendCommands` + validation anti-triche à `EndAttack`). Le serveur fournit le
château (créatures/tiers) et le héros, reçoit les commandes, et réconcilie le butin
(`EndAttackInfo.KillsGold/Xp/LifeForce`). **Faire tourner la simulation 3D** exige
que le moteur natif rende la scène → hôte **Windows ou Wine+GPU réel**. Dans ce
container (CEF sans peinture, pas de GPU), ce n'est pas exécutable. Tout le reste
(protocole, contenu, état) l'est.

## Lancement

```bash
cd server
python3 stub_server.py --host 127.0.0.1 --port 443 --tls   # TLS sur 443
# le client (Wine) pointe dessus via -server_url https://127.0.0.1 (cf. e2e/launch_lobby.sh)
```
`MQ_CATALOG` permet de pointer un autre chemin de catalogue (défaut :
`server/catalog/GameplaySettings`).
