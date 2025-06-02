# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib

# --- Load Dataset ---
def load_adult_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num",
        "marital-status", "occupation", "relationship", "race", "sex",
        "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"
    ]
    df = pd.read_csv(url, header=None, names=column_names, na_values=" ?", skipinitialspace=True)
    df.dropna(inplace=True)  # Drop rows with missing values
    return df

# --- Preprocess and Split ---
def preprocess_data(df):
    df['income'] = df['income'].apply(lambda x: 1 if x == '>50K' else 0)
    
    X = df.drop(columns=['income'])
    y = df['income']

    # Identify column types
    categorical = X.select_dtypes(include=['object']).columns.tolist()
    numerical = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Transformers
    cat_transformer = OneHotEncoder(drop='first', handle_unknown='ignore')
    num_transformer = StandardScaler()

    preprocessor = ColumnTransformer([
        ("num", num_transformer, numerical),
        ("cat", cat_transformer, categorical)
    ])

    return train_test_split(X, y, test_size=0.2, random_state=42), preprocessor

# --- Train Model ---
def train_model():
    df = load_adult_data()
    (X_train, X_test, y_train, y_test), preprocessor = preprocess_data(df)

    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000))
    ])

    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print(f"Test Accuracy: {score:.4f}")

    joblib.dump(clf, "adult_income_model.joblib")
    joblib.dump(X_test.reset_index(drop=True), "X_test.joblib")
    joblib.dump(y_test.reset_index(drop=True), "y_test.joblib")

if __name__ == "__main__":
    train_model()
