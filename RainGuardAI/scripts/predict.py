from sklearn.externals import joblib
import pandas as pd
import json

def load_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def preprocess_input(data):
    # Assuming the input data is a dictionary with relevant features
    # Convert to DataFrame for model input
    df = pd.DataFrame([data])
    return df

def make_prediction(model, input_data):
    processed_data = preprocess_input(input_data)
    prediction = model.predict(processed_data)
    prediction_proba = model.predict_proba(processed_data)
    return prediction[0], prediction_proba

if __name__ == "__main__":
    model_path = '../models/rainfall_model.joblib'
    model = load_model(model_path)

    # Example input data (this should be replaced with actual input)
    input_data = {
        'feature1': value1,
        'feature2': value2,
        # Add all necessary features here
    }

    if model:
        prediction, prediction_proba = make_prediction(model, input_data)
        print(f"Prediction: {prediction}, Probability: {prediction_proba}")