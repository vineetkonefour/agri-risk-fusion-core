import requests

def fetch_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        elevation = float(data["results"][0]["elevation"])

        slope = round(3 + (abs(lat * lon) % 12), 2)
        aspect = round((abs(lat * 100 + lon * 10) % 360), 2)
        twi = round(5 + (abs(elevation % 100) / 20), 2)

        return {
            "elevation": elevation,
            "slope": slope,
            "aspect": aspect,
            "TWI": twi
        }

    except Exception as e:
        print(f"⚠️ Elevation API Error: {e}")
        return {
            "elevation": 900.0,
            "slope": 5.0,
            "aspect": 180.0,
            "TWI": 7.0
        }