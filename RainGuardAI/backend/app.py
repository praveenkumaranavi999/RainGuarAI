from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from datetime import datetime

app = FastAPI(title="RainGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
WEATHER_FILE = BASE_DIR / "data" / "raw" / "latest_weather.json"


@app.get("/")
def home():
    return {
        "project": "RainGuard AI",
        "status": "online",
        "message": "AI Weather & Inundation Prediction API"
    }


@app.get("/status")
def status():
    return {
        "status": "online",
        "ai": "ready"
    }

@app.get("/weather")
def weather():
    try:
        if not WEATHER_FILE.exists():
            return {"error": "Weather data file not found"}

        with open(WEATHER_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)

        # Open-Meteo data is inside data -> current
        weather_data = saved.get("data", {})
        current = weather_data.get("current", {})

        location_data = saved.get("location", {})
        if isinstance(location_data, dict):
            location_name = location_data.get("name", "Coimbatore")
        else:
            location_name = location_data

        return {
            "location": location_name,
            "source": saved.get("source", "Open-Meteo"),
            "rainfall_mm": current.get("rain", 0),
            "precipitation_mm": current.get("precipitation", 0),
            "humidity": current.get("relative_humidity_2m", 0),
            "temperature": current.get("temperature_2m", 0),
            "wind_speed": current.get("wind_speed_10m", 0),
            "forecast_rainfall": 0,
            "updated": current.get("time", "")
        }

    except Exception as e:
        return {
            "error": "Could not read weather data",
            "message": str(e)
        }

@app.get("/risk")
def risk():
    return {
        "location": "Coimbatore",
        "rainfall_risk": "NORMAL",
        "inundation_risk": "LOW",
        "status": "AI READY"
    }