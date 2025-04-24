# backend/app/experts/llava_expert.py
import requests


class LlavaExpert:
    def run(self, prompt, context, **kwargs):
        full = f"[Image Context]\n{context}\nUser:{prompt}\nAssistant:"
        return requests.post("http://localhost:11434/api/generate", json={"model":"llava","prompt":full,**kwargs}).json().get("response","")