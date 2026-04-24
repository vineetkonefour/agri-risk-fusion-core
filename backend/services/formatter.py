NASA_PARAMS = {
    "rainfall": "PRECTOTCORR",
    "temp_min": "T2M_MIN",
    "temp_max": "T2M_MAX",
    "solar_radiation": "ALLSKY_SFC_SW_DWN",
    "wind_speed": "WS2M"
}

OPEN_METEO_PARAMS = {
    "rainfall": "precipitation_sum",
    "temp_min": "temperature_2m_min",
    "temp_max": "temperature_2m_max",
    "solar_radiation": "shortwave_radiation_sum",
    "wind_speed": "wind_speed_10m_max"
}

def normalize_inputs(nasa_data, meteo_data):
    nasa_params = nasa_data.get("properties", {}).get("parameter", {})
    daily = meteo_data.get("daily", {})

    return {
        "history": {
            "rainfall": nasa_params.get("PRECTOTCORR", {}),
            "temp_min": nasa_params.get("T2M_MIN", {}),
            "temp_max": nasa_params.get("T2M_MAX", {}),
            "solar_radiation": nasa_params.get("ALLSKY_SFC_SW_DWN", {}),
            "wind_speed": nasa_params.get("WS2M", {})
        },
        "forecast": {
            "dates": daily.get("time", []),
            "rainfall": daily.get("precipitation_sum", []),
            "temp_min": daily.get("temperature_2m_min", []),
            "temp_max": daily.get("temperature_2m_max", []),
            "solar_radiation": daily.get("shortwave_radiation_sum", []),
            "wind_speed": daily.get("wind_speed_10m_max", [])
        }
    }

def build_feature_row(normalized_data, elevation_data):
    history = normalized_data["history"]
    forecast = normalized_data["forecast"]

    elevation = elevation_data["elevation"]
    slope = elevation_data["slope"]
    aspect = elevation_data["aspect"]
    twi = elevation_data["TWI"]

    rainfall_hist = sum(history["rainfall"].values()) / len(history["rainfall"])

    temp_avg = (
        sum(history["temp_min"].values()) + sum(history["temp_max"].values())
    ) / (2 * len(history["temp_min"]))

    humidity = max(10, min(95, 100 - (temp_avg * 2)))

    solar_rad = sum(history["solar_radiation"].values()) / len(history["solar_radiation"])

    rainfall_7day = sum(forecast["rainfall"])

    temp_min_7day = min(forecast["temp_min"])

    wind_speed = max(forecast["wind_speed"])

    temp_anomaly = temp_avg - 25.0

    rain_deviation = rainfall_7day - rainfall_hist

    north_facing = 1 if aspect >= 315 or aspect <= 45 else 0

    return {
        "elevation": elevation,
        "slope": slope,
        "aspect": aspect,
        "TWI": twi,
        "rainfall_hist": rainfall_hist,
        "temp_avg": temp_avg,
        "humidity": humidity,
        "solar_rad": solar_rad,
        "rainfall_7day": rainfall_7day,
        "temp_min_7day": temp_min_7day,
        "wind_speed": wind_speed,
        "temp_anomaly": temp_anomaly,
        "rain_deviation": rain_deviation,
        "north_facing": north_facing
    }