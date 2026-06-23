@echo off
REM =========================================================================
REM  Lance le serveur MQEL local sur port 13432 (port hardcodé par le jeu)
REM  Laisse cette fenêtre ouverte pendant que tu joues.
REM  Ensuite lance launch_game.bat pour démarrer le jeu.
REM =========================================================================
cd /d "%~dp0"
title MQEL Server (port 13432)

if not exist ".mqel_certs\server.pem" (
    echo [!] Certificats manquants. Lance d'abord setup_windows.bat en admin.
    pause & exit /b 1
)

echo [+] Demarrage du serveur MQEL sur https://0.0.0.0:13432 ...
echo [+] Laisse cette fenetre ouverte pendant que tu joues.
echo.
python stub_server.py --host 0.0.0.0 --port 13432 --tls ^
    --cert .mqel_certs\server.pem ^
    --key  .mqel_certs\server.key
pause
