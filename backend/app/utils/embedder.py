# utils/embedder.py
import requests
from typing import List


def get_embedding(text: str) -> List[float]:
    """
    Get embeddings using Ollama's mxbai-embed-large model
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "mxbai-embed-large",
                "prompt": text
            }
        )
        response.raise_for_status()
        embeddings = response.json().get("embedding", [])
        return embeddings
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []
