import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    """
    Detects anomalies in the sensor data using Isolation Forest.
    """
    # Ensure features exist
    if 'vibration' not in df.columns or 'temperature' not in df.columns:
        return df, 0.0
    
    # Initialize and fit the model
    model = IsolationForest(contamination=0.1, random_state=42)
    features = df[['vibration', 'temperature']]
    
    # Predict (-1 for anomaly, 1 for normal)
    df['anomaly_score'] = model.fit_predict(features)
    df['status'] = df['anomaly_score'].map({1: 'Normal', -1: 'Anomaly'})
    
    # Calculate anomaly ratio
    anomaly_count = (df['status'] == 'Anomaly').sum()
    total_count = len(df)
    anomaly_ratio = anomaly_count / total_count if total_count > 0 else 0.0
    
    return df, anomaly_ratio

def get_risk_level(anomaly_ratio):
    """
    Determines system risk level based on anomaly ratio.
    """
    if anomaly_ratio > 0.3:
        return "HIGH", "🔴"
    elif anomaly_ratio > 0.1:
        return "MEDIUM", "🟡"
    else:
        return "LOW", "🟢"
