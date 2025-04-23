import re
from typing import Optional

def post_process(text: str, original_prompt: str) -> str:
    """Post-process the model response"""
    try:
        # Preserve code blocks
        code_blocks = re.findall(r"```[\s\S]*?```", text)
        
        # Handle special formatting
        text = text.replace("[DONE]", "✅")
        text = text.replace("[ERROR]", "❌")
        
        # Reintegrate code blocks
        for block in code_blocks:
            text = text.replace(block, f"\n{block}\n")
            
        return text
    except Exception as e:
        print(f"Post-processing error: {e}")
        return text