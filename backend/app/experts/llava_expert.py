# experts/llava_expert.py
import requests


class LlavaExpert:
    MODEL = "llava"
    API = "http://localhost:11434/api/generate"

    def run(self, prompt: str, context: str = "") -> str:
        full = f"[Image Context]\n{context}\nUser: {prompt}\nAssistant:"
        resp = requests.post(
            self.API, json={"model": self.MODEL, "prompt": full, "stream": False})
        return resp.json().get("response", "")
