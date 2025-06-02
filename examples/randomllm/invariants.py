from collections import Counter
import math
import numpy as np
from scipy.stats import linregress
from sentence_transformers import SentenceTransformer, util

# Load NLP models once

import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

st_model = SentenceTransformer('all-MiniLM-L6-v2')


# --- Metric Utilities ---

def compute_entropy(text: str) -> float:
    tokens = text.lower().split()
    total = len(tokens)
    freqs = Counter(tokens)
    return -sum((count / total) * math.log2(count / total) for count in freqs.values() if count > 0)

def type_token_ratio(text: str) -> float:
    tokens = text.lower().split()
    types = set(tokens)
    return len(types) / len(tokens) if tokens else 0

def zipf_exponent(text: str) -> float:
    freqs = Counter(text.lower().split())
    sorted_freqs = sorted(freqs.values(), reverse=True)
    if len(sorted_freqs) < 2:
        return 0.0
    ranks = np.arange(1, len(sorted_freqs) + 1)
    log_ranks = np.log(ranks)
    log_freqs = np.log(sorted_freqs)
    slope, _, _, _, _ = linregress(log_ranks, log_freqs)
    return -slope  # Zipf exponent (closer to 1 is better)

def named_entities(text: str) -> set:
    doc = nlp(text)
    return {ent.text for ent in doc.ents}

def ne_overlap(a: str, b: str) -> float:
    ne_a = named_entities(a)
    ne_b = named_entities(b)
    if not ne_a and not ne_b:
        return 1.0
    return len(ne_a & ne_b) / len(ne_a | ne_b)

def semantic_similarity(a: str, b: str) -> float:
    emb_a = st_model.encode(a, convert_to_tensor=True)
    emb_b = st_model.encode(b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b)[0][0])


# --- Chrysalis Invariants ---

def entropy_invariant(curr: str, prev: str) -> bool:
    """Entropy should not deviate more than ±0.5 bits."""
    delta = abs(compute_entropy(curr) - compute_entropy(prev))
    return delta <= 0.5

def lexical_diversity_invariant(curr: str, prev: str) -> bool:
    """Lexical diversity should be stable (within ±0.1)."""
    delta = abs(type_token_ratio(curr) - type_token_ratio(prev))
    return delta <= 0.1

def zipf_invariant(curr: str, prev: str) -> bool:
    """Zipf exponent should stay within ±0.2."""
    delta = abs(zipf_exponent(curr) - zipf_exponent(prev))
    return delta <= 0.2

def named_entity_invariant(curr: str, prev: str) -> bool:
    """Named entities should largely overlap (Jaccard ≥ 0.6)."""
    return ne_overlap(curr, prev) >= 0.6

def semantic_similarity_invariant(curr: str, prev: str) -> bool:
    """Overall meaning should be preserved (cosine similarity ≥ 0.8)."""
    return semantic_similarity(curr, prev) >= 0.8
