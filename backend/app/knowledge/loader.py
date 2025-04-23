# knowledge/loader.py
import re
from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
import os
from utils.embedder import get_embedding


class OllamaEmbeddings:
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using Ollama"""
        return [get_embedding(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed a query using Ollama"""
        return get_embedding(text)


def load_vectorstore():
    if Path("knowledge/vectorstore").exists():
        embeddings = OllamaEmbeddings()
        return FAISS.load_local("knowledge/vectorstore", embeddings)
    raise FileNotFoundError(
        "Vectorstore not found. Run build_vectorstore first."
    )


def search_knowledge(query: str, k: int = 5) -> Optional[List[str]]:
    """Search knowledge base using vector similarity"""
    try:
        embeddings = OllamaEmbeddings()
        vector_store_path = Path("knowledge/vectorstore")

        if not vector_store_path.exists():
            print("Vector store not found. Please build it first.")
            return None

        vectorstore = FAISS.load_local(
            str(vector_store_path),
            embeddings
        )

        results = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    except Exception as e:
        print(f"Error searching knowledge: {e}")
        return None


def extract_algorithms(context: str) -> list[str]:
    # simple regex to find algorithm names Capitalized
    return re.findall(r"Algorithm:\s*(\w+)", context)


def build_vectorstore(source_dir: str = "knowledge/docs"):
    """Build vector store from documents"""
    try:
        # Initialize custom Ollama embeddings
        embeddings = OllamaEmbeddings()

        # Create FAISS vectorstore
        documents = []
        source_path = Path(source_dir)

        if not source_path.exists():
            print(f"Directory not found: {source_dir}")
            return None

        for file_path in source_path.glob('*'):
            try:
                # Try different encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252', 'ascii']:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            text = f.read()
                            documents.append(Document(page_content=text))
                        break  # If successful, break the encoding loop
                    except UnicodeDecodeError:
                        continue  # Try next encoding
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue

        if not documents:
            print("No documents were successfully loaded")
            return None

        # Create vector store directory if it doesn't exist
        vector_store_path = Path("knowledge/vectorstore")
        vector_store_path.mkdir(parents=True, exist_ok=True)

        # Create and save vectorstore
        db = FAISS.from_documents(documents, embeddings)
        db.save_local(str(vector_store_path))
        print(
            f"Successfully built vector store with {len(documents)} documents")
        return db

    except Exception as e:
        print(f"Error building vectorstore: {e}")
        raise
