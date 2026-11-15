@echo off
cd /d "%~dp0"
py -m streamlit run v2\app.py --server.port 8501
pause
