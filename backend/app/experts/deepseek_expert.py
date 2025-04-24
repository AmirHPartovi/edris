# backend/app/experts/deepseek_expert.py
import requests


class DeepseekExpert:
    def run(self, prompt, context, **kwargs):
        full = f"Context:\n{context}\nUser:{prompt}\nAssistant:"
        return requests.post("http://localhost:11434/api/generate", json={"model":"deepseek-r1:latest","prompt":full,**kwargs}).json().get("response","")