import pandas as pd
import json
import os

def create_training_data(raw_data_path, processed_data_path):
    # Load raw weather data
    with open(raw_data_path, 'r') as f:
        raw_data = json.load(f)

    # Process the raw data to create a training dataset
    training_data = []
    for entry in raw_data['weather_data']:
        # Extract relevant features for training
        rainfall = entry.get('rainfall', 0)
        temperature = entry.get('temperature', 0)
        humidity = entry.get('humidity', 0)
        wind_speed = entry.get('wind_speed', 0)
        timestamp = entry.get('timestamp', '')

        training_data.append({
            'rainfall': rainfall,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'timestamp': timestamp
        })

    # Convert to DataFrame
    df = pd.DataFrame(training_data)

    # Save the processed training data
    df.to_csv(processed_data_path, index=False)

if __name__ == "__main__":
    raw_data_path = os.path.join('data', 'raw', 'latest_weather.json')
    processed_data_path = os.path.join('data', 'processed', 'rainfall_training_data.csv')
    create_training_data(raw_data_path, processed_data_path)