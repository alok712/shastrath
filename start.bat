@echo off
title SHASTRATH - Sacred Scripture Arena
cd /d "%~dp0"
echo ========================================================
echo   SHASTRATH - Sacred Scripture Arena
echo   Starting the local server on http://localhost:8765
echo   The browser will open the local game (no waiting).
echo ========================================================
start "" http://localhost:8765
python server.py
pause
