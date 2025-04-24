# knowledge/loader.py

import re
import csv
from pathlib import Path
from typing import List, Optional, Dict, Any
from PIL import Image

import fitz                             # PyMuPDF for PDF text & images
# OCR for scanned PDFs :contentReference[oaicite:0]{index=0}
import pytesseract
# table extraction from PDFs :contentReference[oaicite:1]{index=1}
# import camelot
import python_docx as docx                     # python-docx for .docx text & tables
from langchain.text_splitter import RecursiveCharacterTextSplitter  # chunking
# FAISS vectorstore
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

from app.utils.embedder import get_embedding

# Directory paths
DOCS_DIR = Path("backend/app/knowledge/docs")
VECTORSTORE_DIR = Path("backend/app/knowledge/vectorstore")
IMAGE_CACHE_DIR = Path("backend/app/knowledge/images")

# Ensure directories exist
DOCS_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class OllamaEmbeddings:
    """Embedding interface for Ollama models"""
    
    embedding_dimension: int = 4096  # Default dimension for most Ollama models

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [get_embedding(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return get_embedding(text)

# --- File loaders ---


def load_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_csv_file(path: Path) -> str:
    rows = []
    with path.open(newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(", ".join(row))
    return "\n".join(rows)


def load_pdf_file(path: Path) -> str:
    text_chunks: List[str] = []
    doc = fitz.open(str(path))
    for page in doc:
        txt = page.get_text().strip()
        if txt:
            text_chunks.append(txt)
        else:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr = pytesseract.image_to_string(img)
            text_chunks.append(ocr)
    return "\n".join(text_chunks)


def extract_algorithms(text: str) -> List[str]:
    """Extract algorithm names via multiple regex patterns."""
    patterns = [r"Algorithm:\s*(\w+)", r"(\w+)\s+algorithm",
                r"(?:procedure|method)\s+(\w+)"]
    algos = set()
    for p in patterns:
        for m in re.findall(p, text, flags=re.IGNORECASE):
            algos.add(m.strip())
    return list(algos)


def load_document(path: Path) -> str:
    """Load text from .txt, .md, .csv, .pdf (with OCR), .docx."""
    ext = path.suffix.lower()
    if ext in [".txt", ".md"]:
        return path.read_text(encoding="utf-8", errors="ignore")
    if ext == ".csv":
        rows = []
        with path.open(encoding="utf-8", errors="ignore") as f:
            for row in csv.reader(f):
                rows.append(", ".join(row))
        return "\n".join(rows)
    if ext == ".pdf":
        text_chunks = []
        pdf = fitz.open(str(path))
        for page in pdf:
            t = page.get_text().strip()
            if t:
                text_chunks.append(t)
            else:
                # OCR fallback for scanned page
                pix = page.get_pixmap(dpi=300)
                img = pix.pil_image()  # PIL image
                text_chunks.append(pytesseract.image_to_string(img))
        return "\n".join(text_chunks)
    if ext == ".docx":
        doc = docx.Document(str(path))
        paras = [p.text for p in doc.paragraphs if p.text]
        # extract tables as CSV-like text
        for table in doc.tables:
            for row in table.rows:
                paras.append(", ".join(cell.text for cell in row._cells))
        return "\n".join(paras)
    return ""


def build_vectorstore(source_dir: Path = DOCS_DIR):
    """Read all docs, chunk, embed, and save FAISS index (with metadata)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    # prepare FAISS index
    def embedding_fn(txt): return get_embedding(txt)
    docs: List[Document] = []
    metadatas: List[Dict[str, Any]] = []
    for file in source_dir.rglob("*.*"):
        content = load_document(file)
        for chunk in splitter.split_text(content):
            docs.append(Document(page_content=chunk))
            metadatas.append({
                "source": str(file),
                "algorithms": extract_algorithms(chunk)
            })
    if docs:
        db = FAISS.from_documents(docs, embedding_fn)
        db.save_local(str(VECTORSTORE_DIR))


def search_knowledge(query: str, k: int = 5) -> Optional[List[str]]:
    """Retrieve top-k doc chunks (text) from FAISS index."""
    if not VECTORSTORE_DIR.exists():
        return None

    def embedding_fn(txt): return get_embedding(txt)
    db = FAISS.load_local(str(VECTORSTORE_DIR), embedding_fn)
    results = db.similarity_search(query, k=k)  #
    return [doc.page_content for doc in results]

def load_vectorstore() -> FAISS:
    embeddings = OllamaEmbeddings()
    return FAISS.load_local(VECTORSTORE_DIR, embeddings.embed_query)




if __name__ == "__main__":
    build_vectorstore()
