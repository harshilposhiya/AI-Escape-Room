@echo off
cd /d "%~dp0"
py -m streamlit run v1\app.py --server.port 8502
pause
