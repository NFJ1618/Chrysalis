# transformations.py

import random
from typing import Dict, Any
import nltk
from nltk.corpus import wordnet
import json

# Make sure required NLTK data is downloaded
nltk.download('wordnet')
nltk.download('omw-1.4')

# --- Utility: Synonym Substitution ---
def synonym_replace(word: str) -> str:
    syns = wordnet.synsets(word)
    lemmas = {l.name() for s in syns for l in s.lemmas() if l.name() != word}
    return random.choice(list(lemmas)) if lemmas else word

# --- Transformations ---

# def paraphrase_prompt(prompt: Dict[str, any]) -> Dict[str, any]:
#     """Use the LLM itself to rephrase the instruction."""
#     prompt = prompt.copy()
#     base = prompt.get('instruction', '')
#     wrapper = f"Rephrase this instruction without changing its meaning: \"{base}\""
#     from main_module import ollama_generate_random  # Adjust import based on your structure
#     new_instruction = ollama_generate_random(wrapper, temperature=0.0)
#     prompt['instruction'] = new_instruction.strip()
#     return prompt

def add_irrelevant_context(prompt: Dict[str, Any], context_file: str = "bad_context.json") -> Dict[str, Any]:
    with open(context_file, "r", encoding="utf-8") as file:
        distractors = json.load(file)

    prompt = prompt.copy()
    distractor = random.choice(distractors)
    prompt['instruction'] = f"{distractor} {prompt.get('instruction', '')}"
    return prompt

def add_typo_noise(prompt: Dict[str, any]) -> Dict[str, any]:
    """Introduce light noise with extra spacing and typos."""
    prompt = prompt.copy()
    instr = prompt.get('instruction', '')
    instr = instr.replace(" ", "  ").replace("e", "3", 1)
    prompt['instruction'] = instr
    return prompt

def ask_as_list(prompt: Dict[str, any]) -> Dict[str, any]:
    prompt = prompt.copy()
    prompt['instruction'] = f"{prompt.get('instruction', '')} Format the answer as bullet points."
    return prompt

def ask_as_paragraph(prompt: Dict[str, any]) -> Dict[str, any]:
    prompt = prompt.copy()
    prompt['instruction'] = f"{prompt.get('instruction', '')} Provide the answer as a single paragraph."
    return prompt

def set_low_temp(prompt: Dict[str, any]) -> Dict[str, any]:
    prompt = prompt.copy()
    prompt['temperature'] = 0.2
    return prompt

def set_high_temp(prompt: Dict[str, any]) -> Dict[str, any]:
    prompt = prompt.copy()
    prompt['temperature'] = 1.0
    return prompt

def synonym_substitution(prompt: Dict[str, any]) -> Dict[str, any]:
    prompt = prompt.copy()
    words = prompt.get('instruction', '').split()
    if not words:
        return prompt
    idx = random.randint(0, len(words) - 1)
    words[idx] = synonym_replace(words[idx])
    prompt['instruction'] = ' '.join(words)
    return prompt

def shuffle_prompt_clauses(prompt: Dict[str, any]) -> Dict[str, any]:
    prompt = prompt.copy()
    clauses = prompt.get('instruction', '').split('. ')
    if len(clauses) <= 1:
        return prompt
    random.shuffle(clauses)
    prompt['instruction'] = '. '.join(clauses)
    return prompt