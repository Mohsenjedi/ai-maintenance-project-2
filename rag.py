def analyze_failure(df, anomaly_ratio):
    """
    Rule-based knowledge system to identify failure types.
    """
    if anomaly_ratio > 0.3:
        return {
            "type": "Critical System Failure",
            "cause": "Multiple sensor anomalies detected exceeding acceptable threshold.",
            "solution": "Immediate emergency shutdown and full system inspection required."
        }
    
    # Check individual sensor spikes in the most recent anomalous data
    anomalies = df[df['status'] == 'Anomaly']
    if not anomalies.empty:
        latest_anomaly = anomalies.iloc[-1]
        vibration = latest_anomaly['vibration']
        temperature = latest_anomaly['temperature']
        
        if vibration > 0.7 and temperature > 0.7:
            return {
                "type": "Bearing Failure",
                "cause": "High vibration combined with friction-induced heat.",
                "solution": "Replace bearings and check lubrication levels."
            }
        elif temperature > 0.7:
            return {
                "type": "Overheating",
                "cause": "Thermal runaway or cooling system failure.",
                "solution": "Check coolant levels and ventilation fans."
            }
        elif vibration > 0.7:
            return {
                "type": "Imbalance",
                "cause": "Mechanical misalignment or loose components.",
                "solution": "Perform precision balancing and tighten all fasteners."
            }
    
    return {
        "type": "Normal Operation",
        "cause": "Sensors within operational limits.",
        "solution": "No immediate action required. Continue routine monitoring."
    }
