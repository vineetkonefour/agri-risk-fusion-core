import requests

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

def fetch_nasa_power(lat, lon, start="20240101", end="20241231"):
    params = {
        "parameters": "PRECTOTCORR,T2M_MIN,T2M_MAX,ALLSKY_SFC_SW_DWN,WS2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()