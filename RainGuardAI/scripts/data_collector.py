import requests
import json
from pathlib import Path
from datetime import datetime

LATITUDE = 11.0168
LONGITUDE = 76.9558

OUTPUT_FILE = Path("data/raw/latest_weather.json")

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,

    "current": ",".join([
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "rain",
        "wind_speed_10m"
    ]),

    "hourly": ",".join([
        "precipitation",
        "rain"
    ]),

    "forecast_days": 2,
    "timezone": "Asia/Kolkata"
}


def collect_weather():

    print("Getting live weather data from Open-Meteo...")

    response = requests.get(
        URL,
        params=PARAMS,
        timeout=20
    )

    response.raise_for_status()

    result = response.json()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    weather_data = {
        "location": {
            "name": "Coimbatore",
            "latitude": LATITUDE,
            "longitude": LONGITUDE
        },

        "source": "Open-Meteo",

        "current": result.get("current", {}),

        "hourly": result.get("hourly", {}),

        "retrieved_at_utc": datetime.utcnow().isoformat()
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            weather_data,
            file,
            indent=2
        )

    print("Weather data saved successfully.")
    print("Current weather:")
    print(weather_data["current"])


if __name__ == "__main__":
    collect_weather()