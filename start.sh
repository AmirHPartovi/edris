#!/bin/bash

# Exit on any error
set -e

# Function to check if a process is running on a port
check_port() {
    lsof -i :$1 >/dev/null 2>&1
}

# Create necessary directories
mkdir -p backend/app/{utils,experts,knowledge}
mkdir -p frontend/src/{components,api}

# Setup Python virtual environment
if [ ! -d "backend/.venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv backend/.venv
fi

# Activate virtual environment
source backend/.venv/bin/activate

# Install Python dependencies
echo "Installing backend dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Install Node dependencies
echo "Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    ollama serve &
    sleep 5
fi

# Build vectorstore if not already built
if [ ! -d "backend/app/knowledge/vectorstore" ]; then
    echo "Building vectorstore..."
    source backend/.venv/bin/activate
    python3 -c "from app.knowledge.loader import build_vectorstore; build_vectorstore('backend/app/knowledge/docs')"
fi

# Start backend server
echo "Starting backend server..."
(cd backend && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) &

# Start frontend development server
echo "Starting frontend server..."
(cd frontend && npm run dev) &

# Wait for both servers
wait