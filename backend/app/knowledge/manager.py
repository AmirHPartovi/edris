# File: backend/app/knowledge/manager.py
import json
import os
from pathlib import Path
from typing import Dict, List

from .loader import load_pdf_documents, build_vectorstore as _build_vectorstore

BASE = Path(__file__).resolve().parent
SPACES_DIR = BASE / "spaces"
SPACES_DIR.mkdir(exist_ok=True)


def list_spaces() -> List[Dict]:
    """List all spaces with their metadata."""
    spaces = []
    for space in SPACES_DIR.iterdir():
        if space.is_dir():
            cfg = space / "config.json"
            data = json.loads(cfg.read_text()) if cfg.exists() else {}
            spaces.append({
                "name": space.name,
                "enabled": data.get("enabled", False),
                **data
            })
    return spaces


def create_space(name: str, settings: Dict) -> None:
    """Create a new knowledge space with given settings."""
    space = SPACES_DIR / name
    if space.exists():
        raise FileExistsError(f"Space '{name}' already exists")
    # make directories
    docs = space / "docs"
    vs = space / "vectorstore"
    docs.mkdir(parents=True)
    vs.mkdir()
    # write config
    cfg = space / "config.json"
    cfg.write_text(json.dumps(
        {**settings, "enabled": settings.get("enabled", False)}))


def update_space(name: str, updates: Dict) -> None:
    """Update settings for an existing space."""
    space = SPACES_DIR / name
    cfg = space / "config.json"
    if not cfg.exists():
        raise FileNotFoundError(f"Space '{name}' not found")
    data = json.loads(cfg.read_text())
    data.update(updates)
    cfg.write_text(json.dumps(data))


def delete_space(name: str) -> None:
    """Remove a space entirely."""
    space = SPACES_DIR / name
    if not space.exists():
        raise FileNotFoundError(f"Space '{name}' not found")
    for root, dirs, files in os.walk(space, topdown=False):
        for f in files:
            os.remove(Path(root)/f)
        for d in dirs:
            os.rmdir(Path(root)/d)
    os.rmdir(space)


def build_vectorstore(space: str) -> None:
    """Build the vectorstore for a given space."""
    space_dir = SPACES_DIR / space
    docs_dir = space_dir / "docs"
    vs_dir = space_dir / "vectorstore"
    from app.config import config as global_cfg
    # read space-specific settings
    cfg = space_dir / "config.json"
    settings = json.loads(cfg.read_text())
    # optionally override chunk_size, embeddings, etc.
    _build_vectorstore(str(docs_dir))


def search_knowledge(space: str, query: str, k: int = 5) -> List[str]:
    """Search within a given space."""
    # load vectorstore from space-specific path
    vs_dir = SPACES_DIR / space / "vectorstore"
    # placeholder: load and query vs
    return []
