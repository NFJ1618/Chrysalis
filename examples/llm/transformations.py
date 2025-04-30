import random
from typing import Dict, Any, List

EXPERTISE_MAPPING = {
    1: "You are the worst at mathematics.",
    2: "You are terrible in mathematics.",
    3: "You have a beginners knowledge of mathematics.",
    4: "You are an average mathematics student.",
    5: "You are a professional mathematician.",
    6: "You are a world-class expert in mathematics."
}

MAX_IRRELEVANT_CONTEXT = 50
MIN_IRRELEVANT_CONTEXT = 0

def increase_expertise(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["expertise_level"] < max(EXPERTISE_MAPPING.keys()):
        prompt["expertise_level"] += 1
    return prompt

def decrease_expertise(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["expertise_level"] > min(EXPERTISE_MAPPING.keys()):
        prompt["expertise_level"] -= 1
    return prompt

def expertise_to_system_instruction(prompt: Dict[str, Any]) -> str:
    """Convert expertise_level into the system instruction string."""
    level = prompt.get("expertise_level", 3)
    return EXPERTISE_MAPPING.get(level, "You are a learner of mathematics.")


def increase_irrelevant_context(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["irrelevant_context"] < MAX_IRRELEVANT_CONTEXT:
        prompt["irrelevant_context"] += 10
    return prompt

def decrease_irrelevant_context(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["irrelevant_context"] > MIN_IRRELEVANT_CONTEXT:
        prompt["irrelevant_context"] -= 10
    return prompt

def map_irrelevant_context(prompt: Dict[str, Any], context: List[str], context_weights: List[int]) -> str:
    """Convert context number into sentences."""
    level = prompt.get("irrelevant_context", 0)
    return random.choices(context, weights=context_weights, k=level)
    