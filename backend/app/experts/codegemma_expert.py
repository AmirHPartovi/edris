# experts/codegemma_expert.py
import requests


class CodegemmaExpert:
    MODEL = "codegemma"
    API = "http://localhost:11434/api/generate"

    def run(self, prompt: str, context: str = "") -> str:
        full = f"# Context:\n{context}\n# Request Code for: {prompt}\n# Solution:"
        resp = requests.post(
            self.API, json={"model": self.MODEL, "prompt": full, "stream": False})
        return resp.json().get("response", "")
