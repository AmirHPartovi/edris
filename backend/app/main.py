# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.experts.translator import translate_input, translate_output
from app.utils.router import route_query
from app.knowledge.loader import build_vectorstore, search_knowledge, extract_algorithms
from app.utils.postprocessor import post_process
import os
from utils.router import DOCS_PATH
import logging

#logging
logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)

app = FastAPI()
# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def upload_knowledge(
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...)
):
    # استفاده مستقیم از DOCS_PATH
    DOCS_PATH.mkdir(parents=True, exist_ok=True)

    for f in files:
        out_path = DOCS_PATH / f.filename
        with open(out_path, "wb") as out:
            out.write(await f.read())

    # فراخوانی تابع با پارامتر string مسیر
    background_tasks.add_task(build_vectorstore, str(DOCS_PATH))
    logger.info(f"Received {len(files)} files, scheduled vectorstore build.")
    return {"status": "upload received", "files": [f.filename for f in files]}


@app.get("/health")
async def health(): return {"status": "ok"}