# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.experts.translator import translate_input, translate_output
from app.utils.router import route_query
from app.knowledge.loader import build_vectorstore, search_knowledge, extract_algorithms
from app.utils.postprocessor import post_process
import os

app = FastAPI()
# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')],
    allow_methods=['*'], allow_headers=['*'], allow_credentials=True
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
    # 1. Translate Persian→English if needed
    eng = translate_input(params.prompt)
    # 2. Retrieve top‑5 knowledge docs
    docs = search_knowledge(eng, k=5)
    if not docs:
        return {"response": "[NotFound ❌] No related docs in Knowledge Stack."}
    context = "\n---\n".join(docs)
    # 3. Handle `complete` command with fallback
    # main.py (complete section)
    if eng.lower().startswith("complete"):
        algos = extract_algorithms(context)
        if not algos:
            return {"response": "[NotFound] No algorithm found."}
        # fallback chunking
        if len(context.split()) > 2000:
            context = context.split("\n---\n")[0]
            suggestion = "\nContext too large; showing first part only."
        else:
            suggestion = ""
        raw = route_query(
            f"Explain {algos[0]} step by step", context, model=params.model, **params.dict())
        raw += suggestion+"\nDo you want next algorithm?"
    else:
        raw = route_query(prompt=eng, context=context, input_type=params.type,
                         model=params.model, **params.dict(exclude={'prompt', 'type', 'model'}))
    
    # 5. Post-process formatting
    processed = post_process(raw, params.prompt)
    # 6. Translate back to Persian where appropriate
    final = translate_output(processed, params.prompt)
    return {"response": final}


@app.post("/knowledge/upload")
async def upload_knowledge(files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
    upload_dir = "backend/app/knowledge/docs"
    os.makedirs(upload_dir, exist_ok=True)
    for f in files:
        with open(os.path.join(upload_dir, f.filename), 'wb') as out:
            out.write(await f.read())
            background_tasks.add_task(build_vectorstore, Path(upload_dir))

    return {"status": "upload received", "files": [f.filename for f in files]}


@app.get("/health")
async def health(): return {"status": "ok"}