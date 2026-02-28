from utils.groq_client import run_llm


def run_math_agent(question: str) -> str:
    """
    Math Agent using Groq LLM.
    Designed for step-by-step mathematical reasoning.
    """

    prompt = f"""
You are a mathematics teacher writing solutions in a notebook.

VERY STRICT OUTPUT RULES (NO EXCEPTIONS):
- Output must be line-by-line.
- Press ENTER after EVERY sentence.
- Press ENTER after EVERY formula.
- Never write more than one sentence on the same line.
- Never write formulas inside sentences.
- Do not write paragraphs.
- Use plain text only.
- Do not use markdown, bullets, bold text, or symbols like *, **.

MANDATORY STRUCTURE:
Title

Assumptions
(one assumption per line)

Step 1
(one explanation sentence)
(one formula)

Step 2
(one explanation sentence)
(one formula)

Repeat steps as needed.

Final Answer
(one formula)
{question}
"""

    return run_llm(prompt)