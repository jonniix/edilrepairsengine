@echo off
title Avvio App Verbale
cd /d %~dp0

echo 🔁 Attivazione ambiente virtuale...
call venv\Scripts\activate

echo 🚀 Avvio app Streamlit...
start "" streamlit run app.py --server.port 8080 --server.headless true

echo 🌍 Avvio Ngrok per accesso remoto...
start "" ngrok http 8080

exit
