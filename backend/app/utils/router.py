# utils/router.py
import yaml
from pathlib import Path
from typing import Optional
from experts.deepseek_expert import DeepseekExpert
from experts.codegemma_expert import CodegemmaExpert
from experts.llava_expert import LlavaExpert
from knowledge.loader import search_knowledge

def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

config = load_config()

# Initialize experts
deepseek = DeepseekExpert()
codegemma = CodegemmaExpert()
llava = LlavaExpert()

def route_query(prompt: str, input_type: str = "text") -> str:
    try:
        # Get relevant context
        docs = search_knowledge(prompt, k=5)
        if not docs:
            return "[ERROR] No relevant documents found."
            
        context = "\n---\n".join(docs)
        
        # Route based on input type and content
        if input_type == "image":
            return llava.run(prompt, context)
            
        if any(kw in prompt.lower() for kw in ["code", "algorithm", "function"]):
            return codegemma.run(prompt, context)
            
        return deepseek.run(prompt, context)
        
    except Exception as e:
        print(f"Routing error: {e}")
        return f"[ERROR] {str(e)}"
