import requests
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "rainfall_model.joblib"

LATITUDE = 11.0168
LONGITUDE = 76.9558

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": (
        "precipitation,"
        "relative_humidity_2m,"
        "temperature_2m,"
        "wind_speed_10m"
    ),
    "timezone": "auto",
}


def predict_rainfall_risk():

    print("Getting live weather data...")

    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()

    data = response.json()
    current = data["current"]

    rainfall = current["precipitation"]
    humidity = current["relative_humidity_2m"]
    temperature = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]

    model = joblib.load(MODEL_PATH)

    input_data = pd.DataFrame([{
        "rainfall_mm": rainfall,
        "humidity": humidity,
        "temperature": temperature,
        "wind_speed": wind_speed,
        "previous_rainfall_mm": rainfall
    }])

    prediction = model.predict(input_data)[0]

    print()
    print("===== RainGuard AI =====")
    print("Location: Coimbatore")
    print("Rainfall:", rainfall, "mm")
    print("Humidity:", humidity, "%")
    print("Temperature:", temperature, "C")
    print("Wind Speed:", wind_speed, "km/h")

    if prediction == 1:
        print("AI RESULT: HEAVY RAINFALL RISK")
    else:
        print("AI RESULT: NORMAL RAINFALL")


if __name__ == "__main__":
    predict_rainfall_risk()