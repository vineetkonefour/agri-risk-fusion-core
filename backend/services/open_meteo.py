import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_open_meteo(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_sum,temperature_2m_min,temperature_2m_max,shortwave_radiation_sum,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": 7
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()