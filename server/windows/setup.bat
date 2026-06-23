@echo off
REM ============================================================================
REM  MQEL local server - Windows setup (run as ADMINISTRATOR)
REM  1) points gs.themightyquest.com at this PC (hosts file)
REM  2) trusts the local CA so the game's TLS to gs.themightyquest.com succeeds
REM  Re-runnable; safe to run again.
REM ============================================================================
setlocal
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo [!] Right-click -> "Run as administrator" required. Aborting.
  pause & exit /b 1
)

set HOSTS=%WINDIR%\System32\drivers\etc\hosts
findstr /C:"gs.themightyquest.com" "%HOSTS%" >nul 2>&1
if %errorlevel% neq 0 (
  echo 127.0.0.1 gs.themightyquest.com>> "%HOSTS%"
  echo [+] hosts: added 127.0.0.1 gs.themightyquest.com
) else (
  echo [=] hosts: gs.themightyquest.com already present
)

REM trust our CA (so schannel/curl-using-system-store accepts the server cert)
certutil -addstore -f Root "%~dp0certs\ca.pem" >nul 2>&1
if %errorlevel% equ 0 (echo [+] CA installed into Trusted Root) else (echo [!] CA install failed - see README "TLS" section)

REM flush DNS so the hosts change takes effect immediately
ipconfig /flushdns >nul 2>&1
echo.
echo [ok] setup done. Start the server with run.bat, then launch the game.
pause
