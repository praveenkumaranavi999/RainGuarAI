import json
from datetime import datetime, timezone
from pathlib import Path

import requests

LATITUDE = 11.0168
LONGITUDE = 76.9558

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": (
        "temperature_2m,relative_humidity_2m,precipitation,"
        "rain,showers,weather_code,wind_speed_10m"
    ),
    "hourly": "precipitation,precipitation_probability,rain,showers",
    "forecast_days": 1,
    "timezone": "auto",
}

OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "latest_weather.json"
)


def collect_weather():
    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()

    data = response.json()

    record = {
        "source": "Open-Meteo",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "location": {
            "name": "Coimbatore",
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
        },
        "data": data,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(record, indent=2),
        encoding="utf-8"
    )

    current = data.get("current", {})

    print("OK - live weather data received")
    print("Source:", record["source"])
    print("Location: Coimbatore")
    print("Updated:", current.get("time"))
    print("Rain:", current.get("rain"), "mm")
    print("Precipitation:", current.get("precipitation"), "mm")
    print("Temperature:", current.get("temperature_2m"), "C")
    print("Saved:", OUTPUT)


if __name__ == "__main__":
    try:
        collect_weather()
    except requests.RequestException as exc:
        print("Data connection failed:", exc)
    except Exception as exc:
        print("Unexpected error:", exc)