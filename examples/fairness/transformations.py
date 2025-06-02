# --- Transformation: Flip race between "White" and "Black" for simplicity ---
import random


def flip_race(features: dict) -> dict:
    features = features.copy()
    if features["race"] == "White":
        features["race"] = "Black"
    elif features["race"] == "Black":
        features["race"] = "White"
    return features


# --- Transformation: Flip 'sex' field ---
def flip_gender(features: dict) -> dict:
    features = features.copy()
    if features["sex"] == "Male":
        features["sex"] = "Female"
    elif features["sex"] == "Female":
        features["sex"] = "Male"
    return features


def shift_age(prompt: dict) -> dict:
    prompt = prompt.copy()
    prompt["age"] = max(18, min(90, prompt["age"] + random.choice([-2, 2])))
    return prompt


def shift_hours(prompt: dict) -> dict:
    prompt = prompt.copy()
    delta = random.choice([-5, 5])
    prompt["hours-per-week"] = max(1, prompt["hours-per-week"] + delta)
    return prompt


education_steps = [
    "Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th",
    "11th", "12th", "HS-grad", "Some-college", "Assoc-acdm", "Assoc-voc",
    "Bachelors", "Masters", "Doctorate"
]

def shift_education(prompt: dict) -> dict:
    prompt = prompt.copy()
    edu = prompt["education"]
    if edu in education_steps:
        i = education_steps.index(edu)
        new_i = min(len(education_steps) - 1, max(0, i + random.choice([-1, 1])))
        prompt["education"] = education_steps[new_i]
    return prompt


def tweak_capital_gain(prompt: dict) -> dict:
    prompt = prompt.copy()
    if prompt["capital-gain"] > 0:
        prompt["capital-gain"] += random.randint(-100, 100)
        prompt["capital-gain"] = max(0, prompt["capital-gain"])
    return prompt
