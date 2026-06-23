@echo off
REM ============================================================================
REM  Start the MQEL local server on https://0.0.0.0:443 using the bundled certs.
REM  Run setup.bat once (as admin) first. Keep this window open while playing.
REM  Logs:  trace.jsonl (structured)   requests.log (raw)   state.json (save)
REM  Tip:   add  --debug  for a one-line summary per request in this window.
REM ============================================================================
setlocal
cd /d "%~dp0"
set MQ_TRACE=%~dp0trace.jsonl

if exist mqel_server.exe (
  echo [+] starting mqel_server.exe (port 443, TLS)...
  mqel_server.exe --host 0.0.0.0 --port 443 --tls --cert "%~dp0certs\server.pem" --key "%~dp0certs\server.key" %*
) else (
  echo [+] no exe found, falling back to Python (needs Python 3.10+ installed)...
  python stub_server.py --host 0.0.0.0 --port 443 --tls --cert "%~dp0certs\server.pem" --key "%~dp0certs\server.key" %*
)
pause
