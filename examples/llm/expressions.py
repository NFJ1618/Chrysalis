# IGNORE THIS FILE

import re
import random
import requests
import inflect
from word2number import w2n

p = inflect.engine()

# Flip words ↔ numbers
def flip_token(token):
    if token.isdigit():
        return p.number_to_words(int(token))
    try:
        return str(w2n.word_to_num(token.lower()))
    except:
        return token

# Controlled transformation of expression
def transform_expression(expr, flip_ratio=0.5, seed=None):
    if seed is not None:
        random.seed(seed)

    tokens = re.findall(r'\b\w+\b|\S', expr)
    flippable = []

    for i, t in enumerate(tokens):
        is_num = t.isdigit()
        is_word = False
        if not is_num:
            try:
                w2n.word_to_num(t.lower())
                is_word = True
            except:
                pass
        if is_num or is_word:
            flippable.append(i)

    num_to_flip = max(1, int(len(flippable) * flip_ratio)) if flippable else 0
    indices = random.sample(flippable, num_to_flip)

    for i in indices:
        tokens[i] = flip_token(tokens[i])

    return ' '.join(tokens)

# Template-based wrapping
def wrap_expression(expr, template="What is {expr}? Show your working and then answer with '---Answer: <number>'---."):
    return template.format(expr=expr)

# Call to Ollama API
def ollama_evaluate(prompt, model="mistral", format_prefix="Answer:"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": 0,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        full_output = response.json()["response"]
    except Exception as e:
        return f"{format_prefix} error ({e})"

    # match = re.search(rf'{re.escape(format_prefix)}\s*(.+)', full_output, re.IGNORECASE)
    # return match.group(0) if match else f"{format_prefix} unrecognized"
    return full_output

# Example run
if __name__ == "__main__":
    exprs = [
        "4+3*5-6",
        "7*6-12+3",
        "5*(2+3)",
        "(8+4)*2-3",
        "10+3*(6-2)",
        ]
    for base_expr in exprs:
        for i in range(3):
            transformed = transform_expression(base_expr, flip_ratio=0.5)
            wrapped = wrap_expression(transformed)
            result = ollama_evaluate(wrapped)
            print(f"\nPrompt: {wrapped}\n{result}")