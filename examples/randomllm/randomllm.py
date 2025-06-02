from typing import Dict, Any, List
import json
import chrysalis as chry
from transformations import (
    # paraphrase_prompt,
    add_irrelevant_context,
    shuffle_prompt_clauses,
    synonym_substitution,
    ask_as_paragraph,
    ask_as_list
)
from invariants import (
    entropy_invariant,
    lexical_diversity_invariant,
    zipf_invariant,
    named_entity_invariant,
    semantic_similarity_invariant
)
import requests

DEBUG_LLM_IO = True

# --- SUT: Query model with rephrase instruction ---
def ollama_rephrase(text: str, temperature: float = 0.7) -> str:
    prompt = f"Rephrase the following text. Return your answer only.\n\n{text}"
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3",
        "prompt": prompt,
        "temperature": temperature,
        "stream": False,
    }
    if DEBUG_LLM_IO:
        print("[LLM INPUT]", prompt)
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()["response"]
        if DEBUG_LLM_IO:
            print("[LLM OUTPUT]", result)
        return result.strip()
    except Exception as e:
        if DEBUG_LLM_IO:
            print(f"[LLM ERROR] {e}")
        return "ERROR"

def rephrase_paragraph_sut(prompt_parts: Dict[str, Any]) -> str:
    paragraph = prompt_parts.get("instruction", "")
    temperature = prompt_parts.get("temperature", 0.3)
    return ollama_rephrase(paragraph, temperature)

# --- Input Loader ---
def get_input_data(n: int = 5, file_path: str = "data.json") -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Each entry in the file should be a dict with at least a "paragraph" key
    return [{"instruction": entry["paragraph"], "temperature": 0.5} for entry in data[:n]]

# --- Register Transformations & Invariants ---
# chry.register(paraphrase_prompt, semantic_similarity_invariant)
# chry.register(paraphrase_prompt, zipf_invariant)

chry.register(add_irrelevant_context, named_entity_invariant)
chry.register(add_irrelevant_context, entropy_invariant)
chry.register(add_irrelevant_context, semantic_similarity_invariant)
chry.register(add_irrelevant_context, lexical_diversity_invariant)
chry.register(add_irrelevant_context, zipf_invariant)

chry.register(shuffle_prompt_clauses, named_entity_invariant)
chry.register(shuffle_prompt_clauses, entropy_invariant)
chry.register(shuffle_prompt_clauses, semantic_similarity_invariant)
chry.register(shuffle_prompt_clauses, lexical_diversity_invariant)
chry.register(shuffle_prompt_clauses, zipf_invariant)

chry.register(synonym_substitution, named_entity_invariant)
chry.register(synonym_substitution, entropy_invariant)
chry.register(synonym_substitution, semantic_similarity_invariant)
chry.register(synonym_substitution, lexical_diversity_invariant)
chry.register(synonym_substitution, zipf_invariant)

chry.register(ask_as_paragraph, named_entity_invariant)
chry.register(ask_as_paragraph, entropy_invariant)
chry.register(ask_as_paragraph, semantic_similarity_invariant)
chry.register(ask_as_paragraph, lexical_diversity_invariant)
chry.register(ask_as_paragraph, zipf_invariant)

chry.register(ask_as_list, named_entity_invariant)
chry.register(ask_as_list, entropy_invariant)
chry.register(ask_as_list, semantic_similarity_invariant)
chry.register(ask_as_list, lexical_diversity_invariant)
chry.register(ask_as_list, zipf_invariant)


# --- Run Experiment ---
if __name__ == "__main__":
    chry.run(
        sut=rephrase_paragraph_sut,
        input_data=get_input_data(6),
        chain_length=5,
        num_chains=8
    )
