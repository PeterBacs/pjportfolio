@echo off
cd /d "%~dp0"
if not exist dist\index.html ".venv\Scripts\python.exe" tools\build.py
echo Portfolio running at http://localhost:4173  (close this window to stop)
start "" http://localhost:4173
".venv\Scripts\python.exe" -m http.server 4173 --directory dist
