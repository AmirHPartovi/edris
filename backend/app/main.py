## File: backend/app/main.py
from fastapi import FastAPI, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import List
from utils.router import ChatRequest, ChatResponse , chat_endpoint

from utils.config import (
    BACKEND_HOST, BACKEND_PORT, FRONTEND_ORIGINS,
    DOCS_PATH, SPACES_DIR ,DOCS_PATH, VECTORSTORE_PATH,
    ALGOS_PATH, MEDIA_DIR
)
from knowledge.manager import (
    list_spaces, create_space, delete_space,
    build_space_vs, search_space, search_space_algos
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_methods=["*"], allow_headers=["*"], allow_credentials=True,
)
DOCS_PATH.mkdir(parents=True, exist_ok=True)
VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
ALGOS_PATH.mkdir(parents=True, exist_ok=True)
SPACES_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Serve media files
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


@app.get("/")
async def streamlit():
    return RedirectResponse(url="/docs")

# --- Space Management Endpoints ---
@app.get("/spaces")
def api_list_spaces():
    return {"spaces": list_spaces()}

@app.post("/spaces/{name}")
def api_create_space(name: str, settings: dict):
    create_space(name, settings)
    return {"status": "created", "space": name}

@app.delete("/spaces/{name}")
def api_delete_space(name: str):
    delete_space(name)
    return {"status": "deleted", "space": name}

# --- Knowledge Upload and Build ---
@app.post("/knowledge/upload/{space}")
async def api_upload_and_build(
    background_tasks: BackgroundTasks,
    space: str,
    files: List[UploadFile] = File(...)
):
    docs_dir = SPACES_DIR / space / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        out_path = docs_dir / f.filename
        with open(out_path, "wb") as out:
            out.write(await f.read())
    background_tasks.add_task(build_space_vs, space)
    return {"status": "scheduled", "space": space, "files": [f.filename for f in files]}

# --- Query Endpoints ---
@app.get("/knowledge/search/{space}")
def api_search_knowledge(space: str, q: str, k: int = 5):
    return {"results": search_space(space, q, k)}

@app.get("/algorithms/search/{space}")
def api_search_algorithms(space: str, q: str, k: int = 5):
    return {"algorithms": search_space_algos(space, q, k)}

# --- Health Check ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    return response
# Note: Run Uvicorn with config settings
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)
    # st.run(
    #     streamlit_ui.main,
    #     server_address=BACKEND_HOST,
    #     server_port=BACKEND_PORT,
    #     server_headless=True,
    #     server_enableCORS=False,
    #     server_enableXsrfProtection=False,
    # )

