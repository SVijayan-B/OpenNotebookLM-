@echo off
echo Starting OpenNotebookLM++ ...

echo Starting FastAPI Backend...
start "FastAPI Backend" cmd /c ".\venv\Scripts\Activate.ps1 & uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Waiting for backend to start...
timeout /t 5

echo Starting Streamlit Frontend...
start "Streamlit Frontend" cmd /c ".\venv\Scripts\Activate.ps1 & streamlit run frontend/app.py"

echo Application started! Close the command prompt windows to stop the servers.
pause
