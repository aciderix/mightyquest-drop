@echo off
REM =========================================================================
REM  Setup unique (à lancer en ADMINISTRATEUR une seule fois)
REM  1) Ajoute gs.themightyquest.com -> 127.0.0.1 dans hosts
REM  2) Génère les certificats TLS locaux (.mqel_certs\)
REM  3) Copie notre CA dans le ca.pem du JEU (trust TLS côté jeu)
REM =========================================================================
setlocal
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Clic droit -> "Exécuter en tant qu'administrateur" requis.
    pause & exit /b 1
)

REM 1. hosts
set HOSTS=%WINDIR%\System32\drivers\etc\hosts
findstr /C:"gs.themightyquest.com" "%HOSTS%" >nul 2>&1
if %errorlevel% neq 0 (
    echo 127.0.0.1 gs.themightyquest.com>> "%HOSTS%"
    echo [+] hosts : 127.0.0.1 gs.themightyquest.com ajouté
) else (
    echo [=] hosts : déjà présent
)
ipconfig /flushdns >nul 2>&1

REM 2. Générer les certs si absents
if exist "%~dp0.mqel_certs\server.pem" (
    echo [=] certificats déjà présents
    goto :inject
)
echo [*] Génération des certificats TLS...
python "%~dp0_gen_certs.py"
if %errorlevel% neq 0 (
    echo [!] Echec génération certificats. Python 3.11 installé ?
    pause & exit /b 1
)
echo [+] certificats générés dans .mqel_certs\

:inject
REM 3. Copier notre CA dans le jeu
set GAME_CA=C:\Program Files (x86)\Steam\steamapps\common\The Mighty Quest For Epic Loot\GameData\Bin\ca.pem
if not exist "%GAME_CA%" (
    echo [?] ca.pem du jeu non trouvé : %GAME_CA%
    echo     Chemin différent ? Copie manuellement .mqel_certs\ca.pem dans le dossier Bin du jeu.
    goto :done
)
copy /y "%~dp0.mqel_certs\ca.pem" "%GAME_CA%" >nul
echo [+] ca.pem du jeu remplacé par notre CA (backup : ca.pem.bak si besoin)

:done
echo.
echo [ok] Setup terminé. Lance start_server.bat puis démarre le jeu.
pause
