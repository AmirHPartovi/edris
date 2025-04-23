# Edris MoE-Agent

A multi-expert agent system integrated with a ChatGPT-like frontend, designed to handle various tasks such as knowledge retrieval, translation, and more.

---

## Features

- **Backend**: Built with FastAPI, supports multi-expert routing and knowledge retrieval.
- **Frontend**: React-based ChatGPT-like interface for user interaction.
- **Knowledge Base**: Vectorstore for document search and retrieval.
- **Translation**: Supports Persian-to-English and English-to-Persian translation.
- **Containerization**: Docker support for easy deployment.

---

## Prerequisites

Ensure the following are installed on your system:

- Python 3.9+
- Node.js 16+ and npm
- Docker (optional, for containerized deployment)
- Ollama (for embedding and translation models)

---

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Build the vectorstore for the knowledge base:

   ```bash
   python3 - << 'EOF'
   from app.knowledge.loader import build_vectorstore
   build_vectorstore("app/knowledge/docs")
   EOF
   ```

5. Start the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

### 2. Start Ollama

Ensure Ollama is running to support embeddings and translation models:

```bash
ollama serve &
```

---

### 3. Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install the required Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```

---

## Running with Docker (Optional)

To run the entire application in a containerized environment:

1. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

2. Access the application:
   - **Backend**: [http://localhost:8000](http://localhost:8000)
   - **Frontend**: [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
edris/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── utils/           # Utility modules
│   │   ├── experts/         # Expert modules (e.g., translation)
│   │   ├── knowledge/       # Knowledge base and vectorstore
│   │   └── requirements.txt # Backend dependencies
│   └── Dockerfile           # Backend Docker configuration
├── frontend/
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   ├── vite.config.ts       # Vite configuration
│   └── package.json         # Frontend dependencies
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # Project documentation
```

---

## Environment Variables

### Backend

Create a `.env` file in the `backend` directory with the following variables:

```env
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:3000
OLLAMA_API=http://localhost:11434/api/generate
VECTORSTORE_PATH=app/knowledge/vectorstore
P2E_MODEL=persian-to-english
E2P_MODEL=english-to-persian
```

### Frontend

Create a `.env` file in the `frontend` directory with the following variable:

```env
VITE_SERVER_URL=http://localhost:8000
```

---

## Testing

### Backend

- **Health Check**:

  ```bash
  curl http://localhost:8000/health
  ```

- **Query Endpoint**:
  ```bash
  curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?", "type": "text"}'
  ```

### Frontend

- Open the frontend in your browser:
  ```
  http://localhost:3000
  ```

---

## Debugging

### Common Issues

1. **Port Already in Use**:

   - Find the process using the port:
     ```bash
     lsof -i :8000
     ```
   - Kill the process:
     ```bash
     kill -9 <PID>
     ```

2. **Module Not Found**:

   - Ensure all dependencies are installed:
     ```bash
     pip install -r requirements.txt
     npm install
     ```

3. **Vectorstore Not Built**:
   - Rebuild the vectorstore:
     ```bash
     python3 - << 'EOF'
     from app.knowledge.loader import build_vectorstore
     build_vectorstore("app/knowledge/docs")
     EOF
     ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributors

- **Edris Team** - Core Development
- **Amir Partovi** - Project Lead
