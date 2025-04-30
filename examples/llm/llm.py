from typing import Dict, Any, List
import random
import requests

from transformations import (
    expertise_to_system_instruction,
    increase_expertise,
    decrease_expertise,
    increase_irrelevant_context,
    decrease_irrelevant_context,
    map_irrelevant_context,
)
from generate_expression import generate_math_expression
import chrysalis as chry
from chrysalis import invariants
from functools import cache
import os

# --- Load context --- 
@cache
def get_context():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "context.txt"), "r") as file:
        context = []
        context_weights = []
        for line in file:
            context.append(line)
            try:
                context_weights.append(1/(line.count(" ")+1e6))
            except ZeroDivisionError:
                print(line)
                raise Exception
    return {"context": context, "context_weights": context_weights}


# --- Prompt Construction ---


def stitch_prompt(prompt_parts: Dict[str, Any]) -> str:
    """Assemble a complete prompt from modular parts."""
    sections = [
        expertise_to_system_instruction(prompt_parts),
        prompt_parts.get("irrelevant_context", ""),
        prompt_parts.get("task_instruction", ""),
        prompt_parts.get("examples", ""),
        prompt_parts.get("primary_input", ""),
        prompt_parts.get("formatting_instructions", ""),
        prompt_parts.get("stylistic_requirements", ""),
        prompt_parts.get("meta_information", ""),
    ]
    return "\n\n".join(section for section in sections if section)


# --- LLM Evaluation ---


def ollama_evaluate(
    prompt: str, model: str = "mistral", format_prefix: str = "Answer:"
) -> str:
    """Call Ollama API and return the model's response."""
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "temperature": 0.2, "stream": False}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"{format_prefix} error ({e})"


def ollama_judge(
    problem: str, response: str, correct_answer: str, model="mistral"
) -> str:
    """
    Ask the LLM to judge whether the response matches the correct answer.
    Returns 'yes' or 'no'.
    """
    judge_prompt = f"""
You are a strict grader. 

Problem: {problem}
Model's Response: {response}
Expected Final Answer: {correct_answer}

Only respond with "yes" if the model's final answer matches the expected answer. Respond with "no" otherwise. 
Do not explain. Only say "yes" or "no".
    """.strip()

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": judge_prompt,
        "temperature": 0.0,  # Make judging deterministic
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"].strip().lower()
    except Exception as e:
        # print(f"Judging error: {e}")
        return "no"


# --- Transformation Registration ---

chry.register(increase_expertise, invariants.greater_than_equal)
chry.register(decrease_expertise, invariants.less_than_equal)
chry.register(increase_irrelevant_context, invariants.less_than_equal)
chry.register(decrease_irrelevant_context, invariants.greater_than_equal)


# --- Test Runner ---


def llm_test(prompt_parts: Dict[str, Any], num_tries: int = 1) -> None:
    """Test model consistency by asking LLM to judge its own response."""
    prompt_parts = prompt_parts.copy()
    expected_answer = prompt_parts.get("correct_answer", "").strip()
    prompt_parts["irrelevant_context"] = " ".join(map_irrelevant_context(prompt_parts, **get_context()))
    prompt = stitch_prompt(prompt_parts)
    problem = prompt_parts["primary_input"]
    # print("Prompt:", prompt)
    # print("Expected:", expected_answer)

    correct = 0

    for i in range(num_tries):
        output = ollama_evaluate(prompt)
        # print(f"Output {i+1}:", output)

        judgment = ollama_judge(problem, output, expected_answer)
        # print(f"Judgment {i+1}: {judgment}")

        if judgment == "yes":
            correct += 1

        # print(f"Running Accuracy: {correct / (i + 1):.2%}")

    final_accuracy = correct / num_tries
    # print(
    # f"[Expertise {prompt_parts['expertise_level']}] Final Accuracy: {final_accuracy:.2%} | Target: {expected_answer}"
    # )
    return final_accuracy


# --- Input Generation ---


def get_input_data(n: int = 10) -> List[Dict[str, Any]]:
    """Generate input prompts with varying expertise and random math expressions."""
    base_prompt = {
        "expertise_level": 3,
        "task_instruction": "Solve the following math problem.",
        "examples": "",
        "formatting_instructions": "Show your brief mathematical working without any comments and then give your final answer.",
        "irrelevant_context": 0,
        "stylistic_requirements": "",
        "meta_information": "",
    }

    data = []
    for _ in range(n):
        prompt = base_prompt.copy()
        prompt["expertise_level"] = random.randint(1, 6)
        prompt["irrelevant_context"] = random.randint(0, 5)*10
        expr, correct = generate_math_expression()
        prompt["primary_input"] = expr
        prompt["correct_answer"] = str(correct)
        data.append(prompt)

    return data


if __name__ == "__main__":
    # --- Run All Tests ---
    chry.run(llm_test, get_input_data(1), chain_length=1, num_chains=1)
