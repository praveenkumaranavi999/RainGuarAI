import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "rainfall_training_data.csv"
)

MODEL_PATH = BASE_DIR / "models" / "rainfall_model.joblib"

df = pd.read_csv(DATA_PATH)

X = df[
    [
        "rainfall_mm",
        "humidity",
        "temperature",
        "wind_speed",
        "previous_rainfall_mm",
    ]
]

y = df["heavy_rainfall"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("AI model trained successfully!")
print("Accuracy:", round(accuracy, 4))
print("Model saved:", MODEL_PATH)