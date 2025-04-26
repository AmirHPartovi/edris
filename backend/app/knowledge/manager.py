import json
import os
from pathlib import Path
from typing import Dict, List
from .loader import load_file, build_vectorstore as _build_vectorstore, search_knowledge as _search

BASE = Path(__file__).resolve().parent
SPACES_DIR = BASE / "spaces"
SPACES_DIR.mkdir(exist_ok=True)


def list_spaces() -> List[Dict]:
    """List all spaces with metadata."""
    spaces = []
    for space in SPACES_DIR.iterdir():
        if space.is_dir():
            cfg = space / "config.json"
            data = json.loads(cfg.read_text()) if cfg.exists() else {}
            spaces.append({"name": space.name, **data})
    return spaces


def create_space(name: str, settings: Dict) -> None:
    """Create a new knowledge space."""
    space = SPACES_DIR / name
    if space.exists():
        raise FileExistsError(f"Space '{name}' already exists")
    docs = space / "docs"
    vs = space / "vectorstore"
    docs.mkdir(parents=True)
    vs.mkdir()
    cfg = space / "config.json"
    cfg.write_text(json.dumps({**settings, "enabled": settings.get("enabled", False)}))


def delete_space(name: str) -> None:
    """Remove a space entirely."""
    space = SPACES_DIR / name
    if not space.exists():
        raise FileNotFoundError(f"Space '{name}' not found")
    for root, dirs, files in os.walk(space, topdown=False):
        for f in files:
            os.remove(Path(root) / f)
        for d in dirs:
            os.rmdir(Path(root) / d)
    os.rmdir(space)


def build_vectorstore(space: str) -> None:
    """Build vectorstore for a given space."""
    space_dir = SPACES_DIR / space
    docs_dir = space_dir / "docs"
    vs_dir = space_dir / "vectorstore"
    docs_dir.mkdir(parents=True, exist_ok=True)
    vs_dir.mkdir(parents=True, exist_ok=True)
    # Delegate to loader
    _build_vectorstore(str(docs_dir))


def search_space(space: str, query: str, k: int = 5) -> List[str]:
    """Search within a given space."""
    return _search(query, k)
