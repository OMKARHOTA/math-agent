import re


def parse_problem(text: str):

    cleaned_text = text.strip()
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)

    # Extract variables
    variables = list(set(re.findall(r"[a-zA-Z]", cleaned_text)))

    # Extract constraints
    constraints = re.findall(r"[a-zA-Z]\s*[><=]+\s*\d+", cleaned_text)

    # Topic detection
    topic = "general"

    text_lower = cleaned_text.lower()

    if "probability" in text_lower:
        topic = "probability"

    elif "matrix" in text_lower:
        topic = "linear_algebra"

    elif "derivative" in text_lower:
        topic = "calculus"

    elif "solve" in text_lower:
        topic = "algebra"

    # Check ambiguity
    needs_clarification = False

    if len(cleaned_text.split()) < 3:
        needs_clarification = True

    return {
        "problem_text": cleaned_text,
        "topic": topic,
        "variables": variables,
        "constraints": constraints,
        "needs_clarification": needs_clarification
    }