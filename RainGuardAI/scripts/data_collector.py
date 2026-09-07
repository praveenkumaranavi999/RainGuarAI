import requests
import json
import os

def fetch_live_weather_data():
    # Replace with the actual API endpoint for live weather data
    api_url = "https://api.example.com/weather"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        weather_data = response.json()
        
        # Save the latest weather data to the raw data folder
        raw_data_path = os.path.join(os.path.dirname(__file__), '../data/raw/latest_weather.json')
        with open(raw_data_path, 'w') as json_file:
            json.dump(weather_data, json_file)
        
        print("Successfully fetched and saved live weather data.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live weather data: {e}")

if __name__ == "__main__":
    fetch_live_weather_data()