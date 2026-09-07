import requests

LATITUDE = 11.0168
LONGITUDE = 76.9558

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "precipitation,rain",
    "forecast_days": 1,
    "timezone": "auto",
}


def calculate_inundation_risk():

    print("Getting rainfall forecast...")

    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()

    data = response.json()

    rainfall = data["hourly"]["precipitation"]

    next_6_hours = rainfall[:6]

    total_rainfall = sum(next_6_hours)
    max_rainfall = max(next_6_hours)

    print()
    print("===== RainGuard AI - Inundation Risk =====")
    print("Location: Coimbatore")
    print("Next 6 Hours Rainfall:", round(total_rainfall, 2), "mm")
    print("Maximum Hourly Rainfall:", round(max_rainfall, 2), "mm")

    if total_rainfall >= 100 or max_rainfall >= 50:
        risk = "EXTREME"
    elif total_rainfall >= 60 or max_rainfall >= 30:
        risk = "HIGH"
    elif total_rainfall >= 30 or max_rainfall >= 15:
        risk = "MODERATE"
    else:
        risk = "LOW"

    print("INUNDATION RISK:", risk)


if __name__ == "__main__":
    calculate_inundation_risk()