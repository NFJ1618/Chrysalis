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

COT_MAPPING = {
    0: "Only provide the final answer. Do not show any steps or reasoning.",
    1: "Provide the final answer with one line of working.",
    2: "Show only the few mathematical steps needed to solve the problem. No explanations.",
    3: "For each step, show the calculation and justify what is being done. End with the final answer."
}

MAX_IRRELEVANT_CONTEXT = 50
MIN_IRRELEVANT_CONTEXT = 0
MAX_TEMPERATURE = 0.8
MIN_TEMPERATURE = 0
MIN_COT = 0
MAX_COT = 3

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

def increase_temperature(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["temperature"] < MAX_TEMPERATURE:
        prompt["temperature"] += 0.2
    return prompt

def decrease_temperature(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["temperature"] > MIN_IRRELEVANT_CONTEXT:
        prompt["temperature"] -= 0.2
    return prompt
    
def increase_cot(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["cot"] < MAX_COT:
        prompt["cot"] += 1
    return prompt

def decrease_cot(prompt: Dict[str, Any]) -> Dict[str, Any]:
    prompt = prompt.copy()
    if prompt["cot"] > MIN_COT:
        prompt["cot"] -= 1
    return prompt

def cot_to_system_instruction(prompt: Dict[str, Any]) -> str:
    """Convert expertise_level into the system instruction string."""
    level = prompt.get("cot", 2)
    return COT_MAPPING.get(level, "")