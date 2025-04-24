# backend/app/utils/embedder.py
import requests


def get_embedding(text):
    r = requests.post("http://localhost:11434/api/embeddings",
                      json={"model": "mxbai-embed-large", "prompt": text})
    return r.json().get("embedding", [])