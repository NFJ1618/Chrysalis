# run_fairness_test.py

import joblib
import pandas as pd
import chrysalis as chry
from transformations import (
    flip_gender,
    flip_race,
    shift_age,
    shift_education,
    shift_hours,
    tweak_capital_gain
)
from invariants import (
    label_invariant,
    confidence_invariant,
    gender_bias_invariant,
    race_bias_invariant,
    age_bias_invariant,
    education_bias_invariant
)

# --- Load Trained Model and Data ---
model = joblib.load("adult_income_model.joblib")
X_test = joblib.load("X_test.joblib")

# --- SUT: Predict Income ---
def predict_income(features: dict) -> dict:
    df = pd.DataFrame([features])
    prob = model.predict_proba(df)[0]
    label = int(prob.argmax())
    confidence = float(prob[label])
    return {"label": label, "confidence": confidence, "sex": features["sex"], "race": features["race"], "age": features["age"], "education": features["education"]}

def get_input_data(n: int = 50):
    return X_test.iloc[:n].to_dict(orient="records")

# Register transformations and invariants
chry.register(flip_gender, label_invariant)
chry.register(flip_gender, confidence_invariant)
chry.register(flip_gender, gender_bias_invariant)

chry.register(flip_race, label_invariant)
chry.register(flip_race, confidence_invariant)
chry.register(flip_race, race_bias_invariant)

chry.register(shift_age, label_invariant)
chry.register(shift_age, confidence_invariant)
chry.register(shift_age, age_bias_invariant)

chry.register(shift_education, label_invariant)
chry.register(shift_education, confidence_invariant)
chry.register(shift_education, education_bias_invariant)

chry.register(shift_hours, label_invariant)
chry.register(shift_hours, confidence_invariant)

chry.register(tweak_capital_gain, label_invariant)
chry.register(tweak_capital_gain, confidence_invariant)

if __name__ == "__main__":
    chry.run(
        sut=predict_income,
        input_data=get_input_data(50),
        chain_length=50,
        num_chains=10
    )
