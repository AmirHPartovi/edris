# knowledge/loader.py
import re
from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from app.utils.embedder import get_embedding
from app.config import DOCS_PATH, VECTORSTORE_PATH


def load_text(fp: Path) -> str:
    """Load text content from a file."""
    try:
        return fp.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file {fp}: {e}")
        return ""


def build_vectorstore():
    """Build the vector store from documents."""
    try:
        # Ensure directories exist
        DOCS_PATH.mkdir(parents=True, exist_ok=True)
        VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

        # List all markdown and text files
        files = list(DOCS_PATH.glob("*.md")) + list(DOCS_PATH.glob("*.txt"))
        if not files:
            print(f"No documents found in {DOCS_PATH}")
            return

        # Process documents
        embedder = OllamaEmbeddings()
        documents = [Document(page_content=load_text(fp)) for fp in files]
        db = FAISS.from_documents(documents, embedder)
        db.save_local(str(VECTORSTORE_PATH))
        print("Vector store build completed.")
    except Exception as e:
        print(f"Error building vector store: {e}")


class OllamaEmbeddings:
    """Custom embedding class using Ollama."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return [get_embedding(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed a query."""
        return get_embedding(text)


def load_vectorstore() -> FAISS:
    """Load the vectorstore from the local directory."""
    try:
        if VECTORSTORE_PATH.exists():
            embeddings = OllamaEmbeddings()
            return FAISS.load_local(str(VECTORSTORE_PATH), embeddings)
        raise FileNotFoundError(
            "Vectorstore not found. Run build_vectorstore first.")
    except Exception as e:
        print(f"Error loading vectorstore: {e}")
        raise


def search_knowledge(query: str, k: int = 5) -> Optional[List[str]]:
    """Search the knowledge base using vector similarity."""
    try:
        embeddings = OllamaEmbeddings()
        if not VECTORSTORE_PATH.exists():
            print("Vectorstore not found. Please build it first.")
            return None

        vectorstore = FAISS.load_local(str(VECTORSTORE_PATH), embeddings)
        results = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error searching knowledge: {e}")
        return None



def extract_algorithms(text: str) -> list[str]:

    """
    Placeholder for extracting algorithm names or steps from text.
    """
    # TODO: implement actual algorithm extraction logic
    print(f"Extracting algorithms from text of length {len(text)}")
    return []

if __name__ == "__main__":
    build_vectorstore()
