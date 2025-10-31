import re
def validate_math_query(query: str) -> bool:

    if not query or len(query.strip()) == 0:
        return False


    # block irrevalent characters
    disallowed_patterns=[
        r"import\s+", r"exec\s+", r"os\.system", r"subprocess", r"__"
    ]

    for pattern in disallowed_patterns:
        if re.search(pattern, query):
            return False

    safe_pattern= r"^[0-9a-zA-Z\s\+\-\*\/\^\(\)\=\?\.\,]+$"
    return bool(re.match(safe_pattern, query))

#to clean the model response
def sanitize(response:str) -> str:
    cleaned=re.sub(r"\s+"," ",response)
    cleaned =re.sub(r"^\s+"," ",cleaned)
    return cleaned.strip()

if __name__ == "__main__":
    test_queries = [
        "Solve 2x + 3 = 7",
        "import os; os.system('rm -rf /')",
        "Find derivative of sin(x)^2",
        ""
    ]

    for q in test_queries:
        print(f"\n Query: {q}")
        print("Valid " if validate_math_query(q) else " Invalid")

    resp = "```python\nAnswer = 42\n```"
    print("\nCleaned Output:", sanitize(resp))