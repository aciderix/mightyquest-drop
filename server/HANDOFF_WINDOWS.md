# HANDOFF — Faire booter le vrai jeu MQEL sur Windows (état au 28/06/2026)

Document pour le successeur IA. L'utilisateur est **à distance depuis son téléphone**
— c'est l'IA qui pilote le PC (lance/ferme le jeu, le serveur, lit les logs).

## CONTEXTE
On connecte le **vrai client Windows** `MightyQuest.exe` à notre serveur local
(`stub_server.py`). On a réussi : maintenance OFF → AccountInformation OK →
cinématique → GetCastlesForSale → chargement du Home state (château). On débogue
maintenant les erreurs JSON une par une via le MQLog du jeu.

## CHEMINS CLÉS
- Repo serveur : `C:\Users\fromt\Documents\GitHub\mightyquest-drop\server`
- Jeu : `C:\Program Files (x86)\Steam\steamapps\common\The Mighty Quest For Epic Loot\GameData\Bin`
- **MQLog du jeu** (LA source de vérité du parsing client) : `<Bin>\MQLog.txt`
- Crash reports : `...\The Mighty Quest For Epic Loot\CrashReport\*.breport`
- Ancien serveur (référence, NE PAS réutiliser tel quel mais s'en inspirer) :
  `C:\Users\fromt\Documents\GitHub\The-Mighty-Quest-For-Epic-Loot-port\server`
  - `launcher.py` = mécanique de lancement qui marchait (patch mémoire SSL)
  - `mqel_network.log` = capture d'une vraie session serveur (oracle de types)
  - Doc protocole complète : `C:\Users\fromt\Desktop\ancien server.txt` (à LIRE)

## MÉCANIQUE DE CONNEXION (ce qui marche)
1. **Serveur** sur port **443** TLS (PAS 13432 — c'était l'ancienne version offline).
   Hosts redirige `gs.themightyquest.com → 127.0.0.1` (déjà fait).
   ```
   cd <server>
   python stub_server.py --host 0.0.0.0 --port 443 --tls --cert .mqel_certs\server.pem --key .mqel_certs\server.key
   ```
2. **Certs** : `.mqel_certs\` (CA+server, SAN gs.themightyquest.com). Le CA est
   copié dans `<Bin>\ca.pem` ET `C:\usr\local\ssl\cert.pem` par launch_game.py.
3. **Lancement du jeu** : `python launch_game.py` (PAS Steam !). Il :
   - appelle `/auth` → user_id
   - copie le CA
   - lance `MightyQuest.exe` (ORIGINAL, pas le _mqel) avec
     `-server_url https://127.0.0.1:443 -token "" -steamticket <user_id> -steamid <int64> -environmentName mqel-live -branchName mqel`
   - **patch mémoire SSL à T+20s** (NOP verifypeer/verifyresult de libcurl —
     patterns dans `launch_game.py:_patch_ssl`). SANS ce patch → SSL échoue.
   - `winhttp.dll` (déjà dans <Bin>, depuis l'ancien repo) aide aussi le bypass SSL.

## BOUCLE DE DEBUG (la méthode qui marche)
Le client parse notre réponse JSON champ par champ. Quand un champ a le mauvais
type (liste vs objet vs int), il logge dans MQLog :
```
JSON ERROR: Memory Stream(1,XXXX): Expected character: '[' (ou '{')
OpenOpalPanel : ErrorPanel
Application shutdown ... Reason : OnAccountInformationTaskError Failed
```
**XXXX = position byte (1-based) dans la réponse**. Procédure :
1. Lire la position : `Get-Content "<Bin>\MQLog.txt" | Select-String "JSON ERROR"`
2. Trouver le champ à cette position dans notre réponse :
   ```python
   import ssl,urllib.request
   CTX=ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
   r=urllib.request.Request('https://127.0.0.1:443/AccountService.hqs/GetAccountInformation',data=b'{}',method='POST',headers={'Content-Type':'application/json'})
   txt=urllib.request.urlopen(r,context=CTX,timeout=5).read().decode()
   print(repr(txt[XXXX-30:XXXX+20]))
   ```
3. Si `Expected '['` → le champ doit être une **liste** : ajouter dans
   `re\catalog\network\gamedata\array_fields.json` (liste de noms de champs).
   Si `Expected '{'` → le champ doit être un **objet** : le RETIRER de array_fields,
   ou le forcer à `{}` dans `ep_account_information`.
4. **Redémarrer le serveur** (il charge array_fields au démarrage), relancer le jeu.

## OUTILS PRÊTS
- `auto_fix_loop.py` — boucle autonome : lance jeu → lit MQLog → corrige
  array_fields → recommence. Marche mais CDP (port 9222) ne forward pas toujours,
  donc se fie au MQLog. Lancer : `python auto_fix_loop.py --max-iterations 15`.
  ⚠️ Ne gère que les erreurs `Expected '['/'{'` simples sur AccountInformation.
- `oracle_compare.py` (dans `C:\Users\fromt\AppData\Local\Temp\`) — compare notre
  réponse aux types de la capture `mqel_network.log`. Utile mais la capture n'a
  pas tous les champs (un nouveau joueur diffère).

## CORRECTIONS DÉJÀ FAITES (commits sur claude/funny-gates-79hnf2)
- ClientSettings : tous les URL = "" (MaintenanceUrl="string" → écran maintenance)
- Privileges=9 si pas de héros, 401 sinon
- array_fields ajoutés : HeroCorpses, InventoryDecorations, TrapArchetypes,
  InventoryDefenseIngredientBoosts, UnlockedSpells, RecommendedFriends,
  InventoryThemes, OwnerSpecialPacks, CompletedAchievements, LastViewedDates,
  SpecialPacks, UnlockedAvatars, PendingSharedItems, FakeRewardItems, RewardItems,
  CastleRenovationItems, ConditionGroups (BuyBack RETIRÉ — c'est un objet)
- Objectives/ActiveConsumables/Expirables/FriendshipInvitations/GuildInvitations/
  ShopSkuModifiers = [] pour nouveau joueur (les samples du gate plantaient)
- **starter_build_info()** : nouveau joueur reçoit un BuildInfo.Draft avec heart
  room (sinon crash natif null-deref +0x10 au Home state). MineStatuses={} (objet).

## ÉTAT ACTUEL (28/06/2026 soir) — gros palier atteint
Le jeu **boote entièrement** : TLS → auth → AccountInformation → cinématique →
**StarterCastleSelection** (écran du bouffon), **stable 8+ min, AUCUN crash, AUCUNE
erreur JSON**. Le crash natif 3D historique (`0xC0000005 read [null+0x10] @
0x007DCC57`) est **RÉSOLU**.

### Ce qui a résolu le crash 3D (commits récents)
- **La capture `mqel_network*.log` vient de l'ANCIEN serveur buggé de l'user** →
  vérité = contrats extraits du jeu (`re/catalog/network/schemas_typed.json`,
  `gamedata/enum_*.json`). Toujours cross-checker les types.
- `GetCastlesForSale` doit renvoyer les entrées COMPLÈTES avec `CastleInfoSummary`
  (+ SpawnPlotId, CastleIconUrl, OasisIDs). Champ manquant = le null-deref 3D.
- Nouveau joueur = `no_castle_build_info()` (Draft SANS Rooms, LayoutId 1/ThemeId 2,
  pas de Level) → route vers StarterCastleSelection au lieu d'un Home sans héros
  (qui crashait). DisplayName/SelectedHeroId = null tant que non choisis.
- `GetCastleForSaleBuildInfo` = Pink Castle (1003) = **château TUTO qu'on attaque**
  (a creatures/traps), servi depuis `for_sale_pink_castle.json`. Orientation
  string→int (Left=1,Back=2,Right=3 ; la capture avait des strings buggées).
- `BuyCommand` d'un joueur sans château → accorde le château 2-rooms
  (`starter_castle_buildinfo.json`) + émet CastleBought(86)+Wallet(24)+
  SkusModifiers(90), au lieu de HeroInventoryAddedNotification (qui bouclait).

### BLOCAGE ACTUEL (pause en attendant l'user au clavier)
Le jeu navigue jusqu'à `game://StarterCastleSelection/BuyRandomCastle` puis
**attend une interaction joueur** (choisir/valider le château, saisir le pseudo,
choisir le héros — séquence capture : ChooseDisplayName → ChooseFirstHero →
BuyCommand → StartAttack tutoriel).
**L'UI de cet écran est rendue par le système natif "Opal" (DirectX), PAS le HTML**
→ invisible au screenshot GDI ET à l'inspection CDP (le DOM HTML ne montre que des
panneaux cachés, le champ `.name-input` est dans un parent display:none). Les clics
souris / touches synthétiques n'ont pas touché les boutons Opal. **Pas d'erreur JS,
pas de crash, le jeu ne re-poll rien** → il attend juste l'input réel.
**Prochaine étape** : l'user, au clavier devant l'écran réel, voit l'UI Opal et
interagit (clic château → pseudo → héros). Ensuite débuguer StartAttack tutoriel
(StartAttack/EndAttack contre le Pink Castle 1003). CDP est dispo (port 9222) mais
le CEF est un vieux Chromium (ES5 only, pas d'arrow/spread).

### Outil de diag crash natif (au cas où)
L'exe est packé UBX (`.text` raw=0 sur disque) → désassembler depuis la mémoire du
minidump : parser le `MDMP` dans `CrashReport/*.breport`, lire le CONTEXT x86 +
plage mémoire, capstone (`pip install capstone`). Scripts dans le scratchpad de
session (`parse_dump.py`, `dump_crash.py`).

## RÈGLES IMPORTANTES (de l'utilisateur)
- Ne PAS pousser de PR. Push sur branche `claude/funny-gates-79hnf2` uniquement.
- La vérité = le **catalogue déchiffré** (`server/catalog/GameplaySettings`) + les
  **contrats** (`re/catalog/network/schemas_typed.json`). Les valeurs par défaut
  doivent venir du catalogue (ex. DEFAULTACCOUNT : IGC 1000), pas inventées.
- NE PAS toucher aux valeurs déjà extraites du catalogue sans raison.
- L'utilisateur pilote depuis son téléphone → l'IA lance/ferme tout elle-même.

## COMMANDES UTILES (PowerShell, l'IA a accès au PC)
```powershell
# Etat
Get-Process python,MightyQuest -EA SilentlyContinue | Select Id,StartTime
# Tuer tout
Get-Process MightyQuest,python -EA SilentlyContinue | Stop-Process -Force
# Logs
Get-Content "<Bin>\MQLog.txt" | Select-String "JSON ERROR|ErrorPanel|shutdown.*Reason"
Get-Content "<server>\trace.jsonl"  # requetes recues
```
