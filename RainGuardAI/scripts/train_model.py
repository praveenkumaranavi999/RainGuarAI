# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def load_data(file_path):
    return pd.read_csv(file_path)

def preprocess_data(data):
    # Assuming the target variable is 'rainfall_category' and features are all other columns
    X = data.drop('rainfall_category', axis=1)
    y = data['rainfall_category']
    return X, y

def train_model(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def save_model(model, file_path):
    joblib.dump(model, file_path)

def main():
    # Load the processed training data
    data = load_data('../data/processed/rainfall_training_data.csv')
    
    # Preprocess the data
    X, y = preprocess_data(data)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    predictions = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, predictions))
    print("Classification Report:\n", classification_report(y_test, predictions))
    
    # Save the trained model
    save_model(model, '../models/rainfall_model.joblib')

if __name__ == "__main__":
    main()