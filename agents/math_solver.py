import re
import sympy as sp

def try_math_solver(query: str) -> str:
    q = query.lower().strip()
    # Remove filler words that confuse sympy
    q = re.sub(r'\b(what is|calculate|find|compute|equals?|result of|area of|value of|solve)\b', '', q)
    q = q.strip()

    # Handle "where x = 5" style variable substitution
    variables = dict(re.findall(r'(\w+)\s*=\s*([\d\.]+)', q))
    for var in variables:
        q = re.sub(rf"\b{var}\s*=\s*{variables[var]}\b", '', q)
    q = re.sub(r'\bwhere\b', '', q)

    # Handle patterns like “add 2 and 5”
    patterns = [
        (r'addition of (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?)', r'(\1 + \2)'),
        (r'add (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?)', r'(\1 + \2)'),
        (r'subtract (\d+(?:\.\d+)?) from (\d+(?:\.\d+)?)', r'(\2 - \1)'),
        (r'subtract (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?)', r'(\1 - \2)'),
        (r'multiply (\d+(?:\.\d+)?) by (\d+(?:\.\d+)?)', r'(\1 * \2)'),
        (r'divide (\d+(?:\.\d+)?) by (\d+(?:\.\d+)?)', r'(\1 / \2)'),
        (r'(\d+(?:\.\d+)?) power (\d+(?:\.\d+)?)', r'(\1 ** \2)'),
        (r'square root of (\d+(?:\.\d+)?)', r'sqrt(\1)'),
    ]
    for pat, repl in patterns:
        q = re.sub(pat, repl, q)

    # Replace simple words with symbols
    replacements = {
        "plus": "+", "minus": "-", "times": "*", "x": "*",
        "mod": "%", "modulus": "%", "divided by": "/",
        "power of": "**", "power": "**"
    }
    for word, sym in replacements.items():
        q = re.sub(rf"\b{word}\b", sym, q)

    # Remove assignments like “area =”
    q = re.sub(r'\b\w+\s*=\s*', '', q).strip()

    # Allow safe math functions
    allowed_funcs = {
        "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
        "log": sp.log, "pi": sp.pi, "e": sp.E
    }

    try:
        expr = sp.sympify(q, locals=allowed_funcs)
        if variables:
            subs = {sp.Symbol(k): float(v) for k, v in variables.items()}
            expr = expr.subs(subs)
        result = expr.evalf()
        return f"The answer is {result}"
    except Exception as e:
        return f"Sorry, couldn't solve that expression. ({e})"


if __name__ == "__main__":
    tests = [
        "addition of 2 and 5",
        "add 10 and 20",
        "what is 12 minus 5",
        "multiply 6 by 3",
        "divide 15 by 3",
        "10 power 2",
        "100 mod 3",
        "square root of 81",
        "2 + 5 * 3",
        "area = pi * r^2 where r = 5"
    ]
    for t in tests:
        print(f"{t} → {try_math_solver(t)}")

