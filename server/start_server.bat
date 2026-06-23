@echo off
REM =========================================================================
REM  Lance le serveur MQEL local (depuis le repo, sans exe)
REM  Pré-requis : Python 3.11 installé + setup_windows.bat exécuté une fois
REM  Logs et sauvegarde : dans ce dossier (trace.jsonl, state.json)
REM =========================================================================
cd /d "%~dp0"
title MQEL Server (port 443)

if not exist ".mqel_certs\server.pem" (
    echo [!] Certificats manquants. Lance d'abord setup_windows.bat en admin.
    pause & exit /b 1
)

echo [+] Demarrage du serveur MQEL sur https://0.0.0.0:443 ...
echo [+] Garde cette fenetre ouverte pendant que tu joues.
echo [+] Logs : trace.jsonl / state.json dans ce dossier.
echo.
python stub_server.py --host 0.0.0.0 --port 443 --tls ^
    --cert .mqel_certs\server.pem ^
    --key  .mqel_certs\server.key
pause
