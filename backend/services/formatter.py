import numpy as np

# 1. Historical Baselines (Based on 25-year ICRISAT averages for India)
# These allow the AI to understand if current weather is "Normal" or "Extreme"
HISTORICAL_TEMP_MEAN = 28.5  # average max temp in Celsius
HISTORICAL_RAIN_MEAN = 15.2  # average weekly rainfall in mm during season

def normalize_inputs(nasa_data, meteo_data):
    """
    Cleans and aligns atmospheric data from NASA and Open-Meteo.
    Calculates derived features like 'Anomalies' and 'Deviations'.
    """
    try:
        # Current Atmospheric Values
        temp_avg = meteo_data.get("temp_avg", 25.0)
        rainfall_7day = nasa_data.get("rainfall_7day", 0.0)
        
        # FEATURE 12 & 13: The Intelligence Metrics
        # These tell the model how 'weird' the current weather is
        temp_anomaly = temp_avg - HISTORICAL_TEMP_MEAN
        
        # Deviation calculation (Simple delta for hackathon demo)
        rain_deviation = rainfall_7day - HISTORICAL_RAIN_MEAN

        return {
            "temp_avg": temp_avg,
            "humidity": meteo_data.get("humidity", 60.0),
            "wind_speed": meteo_data.get("wind_speed", 5.0),
            "temp_min_7day": meteo_data.get("temp_min_7day", 20.0),
            "solar_rad": nasa_data.get("solar_rad", 15.0),
            "rainfall_7day": rainfall_7day,
            "temp_anomaly": round(temp_anomaly, 2),
            "rain_deviation": round(rain_deviation, 2)
        }
    except Exception as e:
        print(f"Formatter Normalization Error: {e}")
        return {}

def build_feature_row(normalized, elev_data):
    """
    Combines Terrain data with Atmospheric data into the 
    exact 14-feature order required by the XGBoost models.
    """
    try:
        # Terrain Features from elevation.py
        aspect = elev_data.get("aspect", 0.0)
        
        # FEATURE 14: North Facing (Binary)
        # 1 if aspect is roughly between 315° and 45°, else 0
        north_facing = 1 if (aspect >= 315 or aspect <= 45) else 0

        # Building the final dictionary
        # The keys here must match the keys used in engine/risk_engine.py
        return {
            "elevation": elev_data.get("elevation", 500),
            "slope": elev_data.get("slope", 0.02),
            "aspect": aspect,
            "TWI": elev_data.get("TWI", 8.0), # Topographic Wetness Index
            "rainfall_hist": HISTORICAL_RAIN_MEAN,
            "temp_avg": normalized.get("temp_avg"),
            "humidity": normalized.get("humidity"),
            "solar_rad": normalized.get("solar_rad"),
            "rainfall_7day": normalized.get("rainfall_7day"),
            "temp_min_7day": normalized.get("temp_min_7day"),
            "wind_speed": normalized.get("wind_speed"),
            "temp_anomaly": normalized.get("temp_anomaly"),
            "rain_deviation": normalized.get("rain_deviation"),
            "north_facing": north_facing
        }
    except Exception as e:
        print(f"Formatter Row Building Error: {e}")
        return {}