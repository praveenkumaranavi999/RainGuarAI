def calculate_inundation_risk(forecast_rainfall, max_hourly_rainfall, cumulative_rainfall, rainfall_intensity, elevation=None, drainage_info=None):
    """
    Calculate the inundation risk based on various parameters.
    
    Parameters:
    - forecast_rainfall: float, the predicted rainfall amount
    - max_hourly_rainfall: float, the maximum rainfall in any hour
    - cumulative_rainfall: float, the total rainfall accumulated
    - rainfall_intensity: float, the intensity of the rainfall
    - elevation: float or None, elevation data if available
    - drainage_info: dict or None, drainage/water-body information if available
    
    Returns:
    - risk_level: str, the level of inundation risk (LOW, MODERATE, HIGH, EXTREME)
    - factors: list, main factors contributing to the risk
    """
    
    risk_level = "LOW"
    factors = []

    # Example logic for risk assessment
    if forecast_rainfall > 50:
        risk_level = "HIGH"
        factors.append("High forecast rainfall")
    elif max_hourly_rainfall > 20:
        risk_level = "MODERATE"
        factors.append("High maximum hourly rainfall")
    
    if cumulative_rainfall > 100:
        risk_level = "EXTREME"
        factors.append("High cumulative rainfall")
    
    if rainfall_intensity > 10:
        factors.append("High rainfall intensity")
    
    if elevation is not None and elevation < 100:
        risk_level = "HIGH"
        factors.append("Low elevation increases risk")
    
    if drainage_info and not drainage_info.get("adequate"):
        risk_level = "EXTREME"
        factors.append("Inadequate drainage increases risk")
    
    return risk_level, factors

# This file is intentionally left blank.