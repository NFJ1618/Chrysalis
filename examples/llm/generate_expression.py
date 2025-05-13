import random

MAX_DEPTH = 1 # Depth control: 0 = flat, 1 = slight nesting, etc.

def generate_number() -> str:
    """Generate a number between 1 and 9."""
    return str(random.randint(1, 20))

def generate_factor(depth=0) -> str:
    """Generate a factor: number or (expression), respecting max depth."""
    if depth >= MAX_DEPTH:
        return generate_number()
    # if random.random() < 0.7:
    #     return generate_number()
    return f'{generate_expr(depth + 1)}'

def generate_term(depth=0) -> str:
    """Generate a term: one or more factors multiplied."""
    factors = [generate_factor(depth)]
    while len(factors) < 2 and depth < MAX_DEPTH:
        factors.append(generate_factor(depth))
    return '*'.join(factors)

def generate_expr(depth=0) -> str:
    """Generate an expression: one or more terms added or subtracted."""
    terms = [generate_term(depth)]
    while len(terms) < 2 and depth < MAX_DEPTH:
        op = random.choice(['+', '-'])
        terms.append(op + generate_term(depth))
    return ''.join(terms)

def generate_math_expression() -> tuple[str, int]:
    """Return expression string and its evaluated result."""
    expr = generate_expr()
    return expr, eval(expr)
