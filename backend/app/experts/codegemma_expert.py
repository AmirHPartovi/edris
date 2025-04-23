import requests
from utils.router import OLLAMA_API_URL, EXPERTS_CONFIG


class CodegemmaExpert:
    MODEL = EXPERTS_CONFIG['codegemma']['model']
    API = OLLAMA_API_URL

    def run(self, prompt: str, context: str = "") -> str:
        full = f"# Context:\n{context}\n# Request Code for: {prompt}\n# Solution:"
        resp = requests.post(self.API, json={
            "model": self.MODEL,
            "prompt": full,
            "stream": False
        })
        return resp.json().get("response", "")
