from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# Load the latest weather data
def load_latest_weather():
    try:
        with open(os.path.join("data", "raw", "latest_weather.json")) as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAINGuard AI API"}

@app.get("/status")
def get_status():
    return {"status": "API is running"}

@app.get("/weather")
def get_weather():
    weather_data = load_latest_weather()
    return JSONResponse(content=weather_data)

@app.get("/forecast")
def get_forecast():
    # Placeholder for forecast logic
    return {"forecast": "Forecast data will be implemented"}

@app.get("/prediction")
def get_prediction():
    # Placeholder for prediction logic
    return {"prediction": "Prediction logic will be implemented"}

@app.get("/inundation")
def get_inundation():
    # Placeholder for inundation risk logic
    return {"inundation": "Inundation risk logic will be implemented"}

@app.get("/risk")
def get_risk():
    # Placeholder for risk assessment logic
    return {"risk": "Risk assessment logic will be implemented"}

@app.get("/alerts")
def get_alerts():
    # Placeholder for alerts logic
    return {"alerts": "Alerts logic will be implemented"}

@app.get("/map-data")
def get_map_data():
    # Placeholder for GIS map data logic
    return {"map_data": "GIS map data logic will be implemented"}