from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import urllib.request
import json
from pathlib import Path
import joblib

app = FastAPI(title="RainGuard AI API")

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return {
        "project": "RainGuard AI",
        "status": "online",
        "message": "AI Weather & Inundation Prediction API"
    }


# -----------------------------
# STATUS
# -----------------------------
@app.get("/status")
def status():
    return {
        "ai_status": "ONLINE",
        "project": "RainGuard AI",
        "model": "Random Forest"
    }


# -----------------------------
# WEATHER
# -----------------------------
@app.get("/weather")
def weather():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=11.0168"
        "&longitude=76.9558"
        "&current=temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m"
        "&hourly=precipitation"
        "&forecast_days=1"
    )

    try:

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        current = data["current"]
        hourly = data["hourly"]

        forecast = sum(hourly["precipitation"][:6])

        return {
            "location": "Coimbatore",
            "rainfall_mm": current["precipitation"],
            "precipitation_mm": current["precipitation"],
            "humidity": current["relative_humidity_2m"],
            "temperature": current["temperature_2m"],
            "wind_speed": current["wind_speed_10m"],
            "forecast_rainfall": round(forecast, 2),
            "source": "Open-Meteo",
            "updated": datetime.now().isoformat()
        }

    except Exception as e:

        return {
            "location": "Coimbatore",
            "rainfall_mm": 0,
            "precipitation_mm": 0,
            "humidity": 82,
            "temperature": 25.6,
            "wind_speed": 18.2,
            "forecast_rainfall": 0.2,
            "source": "Demo Fallback",
            "updated": datetime.now().isoformat()
        }


# -----------------------------
# RISK
# -----------------------------
@app.get("/risk")
def risk():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=11.0168"
        "&longitude=76.9558"
        "&hourly=precipitation"
        "&forecast_days=1"
    )

    try:

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        rainfall = data["hourly"]["precipitation"][:6]

        total_rainfall = sum(rainfall)

        max_hourly = max(rainfall) if rainfall else 0

        if total_rainfall >= 60 or max_hourly >= 30:

            rainfall_risk = "HIGH"
            inundation_risk = "HIGH"

        elif total_rainfall >= 30 or max_hourly >= 15:

            rainfall_risk = "MODERATE"
            inundation_risk = "MODERATE"

        else:

            rainfall_risk = "NORMAL"
            inundation_risk = "LOW"

        return {
            "location": "Coimbatore",
            "next_6_hours_rainfall_mm": round(total_rainfall, 2),
            "maximum_hourly_rainfall_mm": round(max_hourly, 2),
            "rainfall_risk": rainfall_risk,
            "inundation_risk": inundation_risk,
            "status": "AI READY"
        }

    except Exception as e:

        return {
            "location": "Coimbatore",
            "next_6_hours_rainfall_mm": 0.2,
            "maximum_hourly_rainfall_mm": 0.1,
            "rainfall_risk": "NORMAL",
            "inundation_risk": "LOW",
            "status": "AI READY"
        }


# -----------------------------
# AI PREDICTION
# -----------------------------
@app.get("/predict")
def predict():

    model_path = Path(__file__).resolve().parents[1] / "models" / "rainfall_model.joblib"

    try:

        model = joblib.load(model_path)

        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=11.0168"
            "&longitude=76.9558"
            "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        )

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        current = data["current"]

        rainfall = current["precipitation"]
        humidity = current["relative_humidity_2m"]
        temperature = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]

        previous_rainfall = rainfall

        features = [[
            rainfall,
            humidity,
            temperature,
            wind_speed,
            previous_rainfall
        ]]

        prediction_value = model.predict(features)[0]

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[0]
            confidence = round(max(probabilities) * 100)
        else:
            confidence = 0

        prediction = (
            "HEAVY RAINFALL"
            if prediction_value == 1
            else "NORMAL RAINFALL"
        )

        return {
            "location": "Coimbatore",
            "prediction": prediction,
            "model": "Random Forest",
            "model_status": "ONLINE",
            "confidence": confidence,
            "source": "Open-Meteo + Rainfall Model",
            "updated": datetime.now().isoformat()
        }

    except Exception as e:

        return {
            "location": "Coimbatore",
            "prediction": "UNAVAILABLE",
            "model": "Random Forest",
            "model_status": "ERROR",
            "confidence": 0,
            "source": "Model unavailable",
            "updated": datetime.now().isoformat()
        }