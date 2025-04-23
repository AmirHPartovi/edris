# utils/router.py
from pathlib import Path
from typing import Optional
import yaml

from experts.deepseek_expert import DeepseekExpert
from experts.codegemma_expert import CodegemmaExpert
from experts.llava_expert import LlavaExpert
from knowledge.loader import search_knowledge

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load configuration from YAML


def load_config() -> dict:
    config_path = BASE_DIR / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config file: {config_path}")
    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


# Load configuration
config = load_config()

# Extract settings from the configuration
OLLAMA_API_URL = config['ollama']['api_url']
DEFAULT_MODEL = config['ollama']['default_model']
DOCS_PATH = Path(config['vectorstore']['docs_path'])
VECTORSTORE_PATH = Path(config['vectorstore']['store_path'])

# Initialize experts
deepseek = DeepseekExpert()
codegemma = CodegemmaExpert()
llava = LlavaExpert()


def route_query(prompt: str, input_type: str = "text") -> str:
    """
    Route the query to the appropriate expert based on the input type and content.
    """
    try:
        # Retrieve relevant documents from the knowledge base
        docs = search_knowledge(prompt, k=5)
        if not docs:
            return "[ERROR] No relevant documents found."

        # Combine documents into a single context
        context = "\n---\n".join(docs)

        # Route based on input type
        if input_type == "image":
            return llava.run(prompt, context)

        # Route based on keywords in the prompt
        if any(keyword in prompt.lower() for keyword in ["code", "algorithm", "function"]):
            return codegemma.run(prompt, context)

        # Default to DeepseekExpert for text-based queries
        return deepseek.run(prompt, context)

    except Exception as e:
        print(f"Routing error: {e}")
        return f"[ERROR] {str(e)}"
