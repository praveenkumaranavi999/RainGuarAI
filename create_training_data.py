import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

rows = 1000

data = {
    "rainfall_mm": np.random.uniform(0, 150, rows),
    "humidity": np.random.uniform(40, 100, rows),
    "temperature": np.random.uniform(20, 35, rows),
    "wind_speed": np.random.uniform(0, 50, rows),
    "previous_rainfall_mm": np.random.uniform(0, 100, rows),
}

df = pd.DataFrame(data)

# Heavy rainfall label
df["heavy_rainfall"] = (
    (df["rainfall_mm"] >= 50) |
    (df["previous_rainfall_mm"] >= 60)
).astype(int)

# Save dataset
output = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "rainfall_training_data.csv"
)

output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)

print("Training dataset created successfully!")
print("Rows:", len(df))
print("Saved:", output)
print(df.head())