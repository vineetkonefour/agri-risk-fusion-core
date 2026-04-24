import requests
from datetime import datetime, timedelta

def get_raw_climate_data(lat, lon):
    # 1. Open-Elevation (Terrain) - Returns elevation in meters
    elev_url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    elevation = requests.get(elev_url).json()['results'][0]['elevation']

    # 2. Open-Meteo (7-Day Forecast) - Sum of daily precipitation in mm
    meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum,temperature_2m_min,wind_speed_10m_max&timezone=auto"
    meteo_data = requests.get(meteo_url).json()['daily']
    
    # 3. NASA POWER (Historical 30-day Avg)
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    nasa_url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR,T2M,RH2M,ALLSKY_SFC_SW_DWN&community=AG&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
    nasa_params = requests.get(nasa_url).json()['properties']['parameter']

    # Package the 11 base features (8 from APIs + 3 GIS placeholders)
    return {
        'elevation': float(elevation),
        'slope': 5.0,     # Placeholder (GIS calculation needed for real value)
        'aspect': 180.0,  # Placeholder (GIS calculation needed for real value)
        'TWI': 7.0,       # Placeholder (Terrain Wetness Index)
        'rainfall_hist': sum(nasa_params['PRECTOTCORR'].values()) * 12, # Annualized mm
        'temp_avg': sum(nasa_params['T2M'].values()) / 30,             # Celsius
        'humidity': sum(nasa_params['RH2M'].values()) / 30,             # %
        'solar_rad': sum(nasa_params['ALLSKY_SFC_SW_DWN'].values()) / 30, # MJ/m2/day
        'rainfall_7day': sum(meteo_data['precipitation_sum']),          # Total mm
        'temp_min_7day': min(meteo_data['temperature_2m_min']),         # Celsius
        'wind_speed': max(meteo_data['wind_speed_10m_max'])             # km/h
    }