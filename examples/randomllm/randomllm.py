from typing import Dict, Any, List
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
    temperature = prompt_parts.get("temperature", 0.7)
    return ollama_rephrase(paragraph, temperature)

# --- Input Loader ---
def get_input_data(n: int = 5) -> List[Dict[str, Any]]:
    # Substitute with actual text samples
    base_paragraphs = [
        "Climate change refers to long-term alterations in temperature, precipitation, wind patterns, and other elements of the Earth's climate system. While some of these changes occur naturally due to volcanic eruptions or solar cycles, the rapid changes observed in recent decades are largely attributed to human activities such as burning fossil fuels and deforestation. These activities increase greenhouse gas concentrations in the atmosphere, which trap heat and lead to global warming. The consequences include rising sea levels, more extreme weather events, and disruptions to ecosystems and agriculture.",
        
        "The mitochondrion, often called the powerhouse of the cell, is an organelle responsible for generating most of the cell's supply of adenosine triphosphate (ATP), the molecule used for energy transfer within cells. Mitochondria play a crucial role in cellular respiration, converting oxygen and nutrients into ATP through a series of biochemical reactions. Beyond energy production, mitochondria are also involved in other essential processes such as signaling, cellular differentiation, and cell death. Their dysfunction is linked to a variety of diseases, including neurodegenerative disorders and metabolic syndromes.",
        
        "William Shakespeare’s influence on the English language and literature is both deep and enduring. His works, including plays, sonnets, and poems, introduced thousands of words and expressions still in use today. Shakespeare shaped dramatic structure and character development in ways that continue to influence modern storytelling, from stage to screen. His exploration of themes such as ambition, identity, love, and betrayal transcends time and culture. Even in contemporary cinema and television, echoes of his plots and dialogue are frequently found.",
        
        "Photosynthesis is a vital biochemical process through which green plants, algae, and certain bacteria convert sunlight into chemical energy. By using sunlight to transform carbon dioxide and water into glucose and oxygen, these organisms form the foundation of most food chains on Earth. The process takes place in the chloroplasts of plant cells and is essential for maintaining atmospheric oxygen levels. In addition to sustaining life, photosynthesis plays a critical role in regulating the Earth’s carbon cycle and mitigating climate change.",
        
        "The Great Wall of China is a massive structure built over centuries to protect Chinese states and empires from nomadic invasions and raids. Stretching thousands of miles across varied terrain, it includes walls, watchtowers, and fortresses constructed from stone, brick, tamped earth, and wood. Though not a single continuous wall, its various sections collectively represent a monumental feat of engineering and organization. Beyond its military function, the Wall also facilitated trade, border control, and cultural integration along the Silk Road. Today, it stands as a symbol of China’s historical strength and perseverance."
    ]

    return [{"instruction": text, "temperature": 0.5} for text in base_paragraphs[:n]]

# --- Register Transformations & Invariants ---
# chry.register(paraphrase_prompt, semantic_similarity_invariant)
# chry.register(paraphrase_prompt, zipf_invariant)

chry.register(add_irrelevant_context, named_entity_invariant)
chry.register(add_irrelevant_context, entropy_invariant)

chry.register(shuffle_prompt_clauses, semantic_similarity_invariant)
chry.register(shuffle_prompt_clauses, lexical_diversity_invariant)

chry.register(synonym_substitution, entropy_invariant)
chry.register(synonym_substitution, zipf_invariant)

chry.register(ask_as_paragraph, semantic_similarity_invariant)
chry.register(ask_as_list, lexical_diversity_invariant)

# --- Run Experiment ---
if __name__ == "__main__":
    chry.run(
        sut=rephrase_paragraph_sut,
        input_data=get_input_data(1),
        chain_length=1,
        num_chains=1
    )
