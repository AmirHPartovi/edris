# knowledge/loader.py
import re
from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from app.utils.embedder import get_embedding
from app.utils.router import DOCS_PATH, VECTORSTORE_PATH


def load_text(fp: Path) -> str:
    """Load text content from a file."""
    try:
        return fp.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file {fp}: {e}")
        return ""


def build_vectorstore():
    """Build the vectorstore from documents."""
    try:
        # Ensure directories exist
        DOCS_PATH.mkdir(parents=True, exist_ok=True)
        VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

        # List all markdown and text files
        files = list(DOCS_PATH.glob("*.md")) + list(DOCS_PATH.glob("*.txt"))

        # Process files in batches
        batch_size = 10
        for i in range(0, len(files), batch_size):
            batch = files[i: i + batch_size]
            texts = [load_text(fp) for fp in batch]
            print(
                f"Processing batch {i // batch_size + 1}: {[fp.name for fp in batch]}")

        print("Vectorstore build completed.")
    except Exception as e:
        print(f"Error building vectorstore: {e}")


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


def extract_algorithms(context: str) -> List[str]:
    """Extract algorithm names from the context."""
    return re.findall(r"Algorithm:\s*(\w+)", context)


def build_vectorstore_from_source(source_dir: str = "knowledge/docs"):
    """Build the vectorstore from a specified source directory."""
    try:
        embeddings = OllamaEmbeddings()
        documents = []
        source_path = Path(source_dir)

        if not source_path.exists():
            print(f"Directory not found: {source_dir}")
            return None

        for file_path in source_path.glob('*'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    documents.append(Document(page_content=text))
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue

        if not documents:
            print("No documents were successfully loaded.")
            return None

        VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
        db = FAISS.from_documents(documents, embeddings)
        db.save_local(str(VECTORSTORE_PATH))
        print(
            f"Successfully built vectorstore with {len(documents)} documents.")
        return db
    except Exception as e:
        print(f"Error building vectorstore: {e}")
        raise


if __name__ == "__main__":
    build_vectorstore()
