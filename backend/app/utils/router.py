# backend/app/utils/router.py
from app.experts.deepseek_expert import DeepseekExpert
from app.experts.codegemma_expert import CodegemmaExpert
from app.experts.llava_expert import LlavaExpert
from app.knowledge.loader import search_knowledge

# threshold for context size fallback
MAX_TOKENS = 2000
CODE_KWS = ["code", "function", "script", "pseudo"]


def route_query(prompt, context, input_type="text", model=None, **kwargs):
    # choose expert
    if input_type == "image":
        expert = LlavaExpert()
    elif any(kw in prompt.lower() for kw in CODE_KWS):
        expert = CodegemmaExpert()
    else:
        expert = DeepseekExpert()
    # run with parameters, include context in prompt
    answers = []
    docs = search_knowledge(prompt, k=5)  # top-5


    for doc in docs:
        answers.append(expert.run(
            prompt=prompt, context=doc, model=model, **kwargs))
    return "\n---\n".join(answers)
