@echo off
REM ============================================================================
REM  Analyse trace.jsonl and print what likely caused an in-game problem.
REM  Run AFTER reproducing the issue (the server must have logged it).
REM  Examples:
REM     diagnose.bat                 full summary (errors, fallbacks, rejects)
REM     diagnose.bat --tail 40       last 40 requests
REM     diagnose.bat --grep Guild    only requests mentioning "Guild"
REM     diagnose.bat --symptom       symptom -> where to look
REM  Copy this window's output to the AI together with what you did in-game.
REM ============================================================================
setlocal
cd /d "%~dp0"
set MQ_TRACE=%~dp0trace.jsonl
if exist mqel_server.exe (mqel_server.exe diagnose %*) else (python diagnose.py %*)
echo.
pause
