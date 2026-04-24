import requests
from datetime import datetime, timedelta

def fetch_nasa_power(lat, lon):
    """
    Fetches Solar Radiation and Rainfall data from NASA POWER API.
    """
    # 1. Define the 7-day window for rainfall accumulation
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')

    # Parameters: 
    # ALLSKY_SFC_SW_DWN = Solar Radiation
    # PRECTOTCORR = Corrected Precipitation (Rainfall)
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN,PRECTOTCORR&community=AG&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Extract features
        solar_values = list(data['properties']['parameter']['ALLSKY_SFC_SW_DWN'].values())
        rain_values = list(data['properties']['parameter']['PRECTOTCORR'].values())

        return {
            "solar_rad": sum(solar_values) / len(solar_values) if solar_values else 15.0,
            "rainfall_7day": sum(rain_values) if rain_values else 0.0,
            "raw_nasa": data['properties']['parameter']
        }
    except Exception as e:
        print(f"NASA POWER Error: {e}")
        return {"solar_rad": 15.0, "rainfall_7day": 0.0, "error": str(e)}