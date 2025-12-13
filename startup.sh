#!/bin/bash
# startup.sh - Script to start the RAG chatbot backend

# Navigate to the backend directory
cd "$(dirname "$0")/backend"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Checking environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env with your actual credentials before running the server"
    exit 1
fi

echo "Starting the RAG chatbot backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000