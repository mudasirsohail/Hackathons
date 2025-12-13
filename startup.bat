@echo off
REM startup.bat - Script to start the RAG chatbot backend

cd /d "%~dp0\backend"

echo Installing dependencies...
pip install -r requirements.txt

echo Checking environment variables...
if not exist .env (
    echo Creating .env file from example...
    copy .env.example .env
    echo Please edit .env with your actual credentials before running the server
    pause
    exit /b 1
)

echo Starting the RAG chatbot backend server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause