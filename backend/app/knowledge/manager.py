import json
from pathlib import Path
from typing import Dict, List
from knowledge.loader import load_file, build_vectorstore, extract_algorithms
from knowledge.loader import build_vectorstore as _build_vs, build_vectorstore as _build_algos
from utils.config import SPACES_DIR, DOCS_PATH, VECTORSTORE_PATH, ALGOS_PATH, MEDIA_DIR
from utils.embedder import get_embedding
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS

BASE = Path(__file__).resolve().parent
SPACES_DIR = BASE / "spaces"



# Spaces folder
SPACES_DIR.mkdir(exist_ok=True)

def list_spaces() -> List[Dict]:
    spaces = []
    for space in SPACES_DIR.iterdir():
        if space.is_dir():
            cfg = space / "config.json"
            data = json.loads(cfg.read_text()) if cfg.exists() else {}
            spaces.append({"name": space.name, **data})
    return spaces

def create_space(name: str, settings: Dict) -> None:
    space = SPACES_DIR / name
    if space.exists(): raise FileExistsError(f"Space '{name}' exists.")
    (space / "docs").mkdir(parents=True)
    (space / "vectorstore").mkdir()
    (space / "config.json").write_text(json.dumps(settings))

def delete_space(name: str) -> None:
    space = SPACES_DIR / name
    if not space.exists(): raise FileNotFoundError(f"Space '{name}' not found.")
    for p in space.rglob("*"): p.unlink() if p.is_file() else None
    for d in sorted((space).iterdir(), key=lambda x: x.is_file()): d.rmdir()

# Build both docs and algos for a space
def build_space_vs(name: str) -> None:
    docs_dir = SPACES_DIR / name / "docs"
    media_dir = MEDIA_DIR
    media_dir.mkdir(parents=True, exist_ok=True)
    _build_vs(str(docs_dir))
    _build_algos(str(docs_dir))

# Search within text docs
def search_space(name: str, query: str, k: int = 5) -> List[str]:
    vs_dir = SPACES_DIR / name / "vectorstore"
    if not vs_dir.exists(): return []
    db = FAISS.load_local(str(vs_dir), get_embedding)
    return [d.page_content for d in db.similarity_search(query, k=k)]

# Search within algorithms
def search_space_algos(name: str, query: str, k: int = 5) -> List[str]:
    algo_dir = SPACES_DIR / name / "vectorstore" / "algos"
    if not algo_dir.exists(): return []
    db = FAISS.load_local(str(algo_dir), get_embedding)
    return [d.page_content for d in db.similarity_search(query, k=k)]