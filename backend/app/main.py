# main.py
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from experts.translator import translate_input, translate_output
from utils.router import route_query
from knowledge.loader import build_vectorstore, search_knowledge, extract_algorithms
import os
import requests

OLLAMA_API = "https://api.ollama.ai"
P2E_MODEL = "persian-to-english"
E2P_MODEL = "english-to-persian"

app = FastAPI()
# CORS to allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        'FRONTEND_ORIGINS', 'http://localhost:5173').split(','),
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)


class ChatParams(BaseModel):
    prompt: str
    type: str = "text"
    model: str = "deepseek-r1:latest"
    temperature: float = 0.2
    max_tokens: int = 512
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: list[str] = ["\n\n"]
    stream: bool = False


@app.post("/query")
async def query_agent(params: ChatParams):
    try:
        # Step 1: Translate input if Persian
        eng = translate_input(params.prompt)
        # Step 2: Retrieve context
        docs = search_knowledge(eng, k=5)
        if not docs:
            return {"response": "[NotFound ❌] Documents not found in Knowledge Stack."}
        context = "\n---\n".join(docs)
        # Step 3: Route to expert with model params
        raw = route_query(prompt=eng, input_type=params.type)
        # Step 4: Post-process and translate back
        from utils.postprocessor import post_process
        processed = post_process(raw, params.prompt)
        final = translate_output(processed, params.prompt)
        return {"response": final}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing query: {str(e)}"
        )


@app.post("/knowledge/upload")
async def upload_knowledge(
    files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = None
):
    try:
        # Save uploaded docs and rebuild vectorstore
        upload_dir = "knowledge/docs"
        os.makedirs(upload_dir, exist_ok=True)
        for f in files:
            path = os.path.join(upload_dir, f.filename)
            with open(path, 'wb') as out:
                out.write(await f.read())

        # Rebuild vectorstore in the background
        def rebuild():
            try:
                build_vectorstore(source_dir=upload_dir)
            except Exception as e:
                print(f"Error rebuilding vectorstore: {e}")

        background_tasks.add_task(rebuild)
        return {"status": "upload received", "files": [f.filename for f in files]}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading knowledge: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )
