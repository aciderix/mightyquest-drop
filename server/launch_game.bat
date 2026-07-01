@echo off
REM =========================================================================
REM  Lance le jeu via le launcher local (après start_server.bat)
REM  Ne pas lancer le jeu depuis Steam — utiliser ce script.
REM =========================================================================
cd /d "%~dp0"
echo [*] Connexion au serveur local et lancement du jeu...
python launch_game.py
pause
