@echo off
cd /d %~dp0
call venv\Scripts\activate
git add .
git commit -m "🚀 Aggiornamento automatico"
git push
pause
