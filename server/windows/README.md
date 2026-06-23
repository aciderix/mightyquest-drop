# MQEL local server — tester sur PC contre le vrai jeu (Windows)

Ce dossier permet de faire tourner le serveur local en face du **vrai client
Windows** de *The Mighty Quest for Epic Loot*, avec un **traçage complet** pour
qu'une IA retrouve la cause de n'importe quel bug in-game.

## Contenu (release)
```
mqel_server.exe        le serveur (ou stub_server.py + Python si pas d'exe)
catalog\GameplaySettings\   le contenu réel du jeu (déchiffré)
re\catalog\network\    schémas/enums (embarqués dans l'exe ; présents ici pour la version Python)
certs\ ca.pem server.pem server.key   PKI locale (SAN gs.themightyquest.com)
setup.bat  run.bat     scripts
diagnose.py            outil de diagnostic (lecture de trace.jsonl)
```

## Démarrage (3 étapes)
1. **`setup.bat`** en **administrateur** — ajoute `127.0.0.1 gs.themightyquest.com`
   au fichier hosts et installe le CA local dans « Autorités de certification
   racines de confiance ».
2. **`run.bat`** — démarre le serveur sur `https://0.0.0.0:443` (laisse la fenêtre
   ouverte). Ajoute `--debug` pour voir une ligne par requête.
3. **Lance le jeu** normalement. Le client appelle `gs.themightyquest.com` → 127.0.0.1.
   S'il faut forcer l'URL : `MightyQuest.exe -server_url https://gs.themightyquest.com`.

## TLS — si le jeu refuse la connexion
Le client de 2014 peut soit utiliser le magasin Windows (alors `setup.bat` suffit),
soit un **curl avec un bundle CA embarqué**. Dans ce 2e cas :
- cherche dans le dossier du jeu un fichier `cacert.pem` / `ca-bundle.crt` /
  `curl-ca-bundle.crt` et **remplace son contenu** par celui de `certs\ca.pem`
  (ou ajoute-le à la fin) ;
- variante : copie `certs\ca.pem` à l'emplacement attendu par le binaire.
Si la connexion échoue toujours, c'est un **problème de confiance TLS** (pas un bug
serveur) : note-le tel quel, c'est une piste connue.

## Signaler un bug pour l'IA (important)
Quand quelque chose cloche en jeu :
1. **garde `trace.jsonl`** (à côté du serveur) — chaque requête y est enregistrée ;
2. lance le diagnostic :
   ```
   python diagnose.py                 (résumé : erreurs, fallbacks, rejets)
   python diagnose.py --tail 40       (les 40 dernières requêtes)
   python diagnose.py --grep Guild    (filtrer sur un service/fonction)
   python diagnose.py --symptom       (aide symptôme -> où chercher)
   ```
3. **colle la sortie de `diagnose.py` + ta description** ("j'ai cliqué X, il s'est
   passé Y"). Chaque ligne pointe le fichier/handler à regarder.

Une IA sans contexte peut alors : repérer la requête fautive, voir si la réponse
venait d'un **fallback statique** (cause n°1 d'un écran inerte) ou d'un **rejet de
commande** (ex. équipement mauvais slot), et corriger localement. Voir
`../AI_GUIDE.md` pour le fonctionnement complet du pipeline.

## Fichiers produits par le serveur
- `trace.jsonl` — trace structurée (la source de vérité pour le debug)
- `requests.log` — journal brut des requêtes
- `state.json` — sauvegarde (compte, héros, château, social) ; supprime-le pour repartir de zéro
- `uncertain.log` — valeurs d'enum incertaines rencontrées (à corréler à un bug)

## Limites connues (pas des bugs serveur)
- La **simulation de combat 3D** tourne dans le moteur natif du jeu (pas dans le
  serveur) ; si le combat 3D plante, c'est côté client/Windows, pas côté serveur.
- Services temps-réel non couverts (chat, replay, événements live) → réponses
  d'exemple (inertes) ; visibles comme `fallback_example` dans `diagnose.py`.
