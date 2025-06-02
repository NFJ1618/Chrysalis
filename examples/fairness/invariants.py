# --- Invariant: Confidence should not drop more than 15% ---
def confidence_invariant(curr: dict, prev: dict, tolerance: float = 0.15) -> bool:
    prev_conf = prev["confidence"]
    curr_conf = curr["confidence"]

    # Avoid division by zero
    if prev_conf == 0:
        return curr_conf == 0

    # Allow confidence to change within ±15%
    ratio = curr_conf / prev_conf
    return 1 - tolerance <= ratio <= 1 + tolerance


def label_invariant(curr: dict, prev: dict) -> bool:
    return curr["label"] == prev["label"]


# invariants.py

def gender_bias_invariant(curr: dict, prev: dict) -> bool:
    # Hypothesis: Model gives higher confidence to males
    if prev["sex"] == "Female" and curr["sex"] == "Male":
        return curr["confidence"] <= prev["confidence"] + 0.01
    return True  # skip or return True if not the relevant transition

def race_bias_invariant(curr: dict, prev: dict) -> bool:
    # Hypothesis: Model favors white over Black
    if prev["race"] == "Black" and curr["race"] == "White":
        return curr["confidence"] <= prev["confidence"] + 0.01
    return True

def age_bias_invariant(curr: dict, prev: dict) -> bool:
    # Hypothesis: Model favors older individuals (>40) for higher income
    return not (prev["age"] < 40 <= curr["age"] and curr["confidence"] > prev["confidence"] + 0.05)

def education_bias_invariant(curr: dict, prev: dict) -> bool:
    # Hypothesis: Model significantly increases prediction confidence for higher education
    edu_levels = {
        "Preschool": 0, "1st-4th": 1, "5th-6th": 2, "7th-8th": 3, "9th": 4,
        "10th": 5, "11th": 6, "12th": 7, "HS-grad": 8, "Some-college": 9,
        "Assoc-acdm": 10, "Assoc-voc": 11, "Bachelors": 12,
        "Prof-school": 13, "Masters": 14, "Doctorate": 15
    }

    if edu_levels[prev["education"]] < edu_levels[curr["education"]]:
        return curr["confidence"] <= prev["confidence"] + 0.10
    return True
