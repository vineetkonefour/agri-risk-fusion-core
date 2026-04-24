from services.nasa_power import fetch_nasa_power
from services.open_meteo import fetch_open_meteo
from services.elevation import fetch_elevation
from services.formatter import normalize_inputs, build_feature_row

def test_all_apis():
    lat = 12.9716
    lon = 77.5946

    print("Testing APIs for location:")
    print("Latitude:", lat)
    print("Longitude:", lon)
    print("-" * 50)

    print("1. Fetching NASA POWER data...")
    nasa_data = fetch_nasa_power(lat, lon)
    print("NASA data received.")
    print("NASA keys:", nasa_data.keys())
    print("-" * 50)

    print("2. Fetching Open-Meteo data...")
    meteo_data = fetch_open_meteo(lat, lon)
    print("Open-Meteo data received.")
    print("Open-Meteo keys:", meteo_data.keys())
    print("-" * 50)

    print("3. Fetching Open-Elevation data...")
    elev_data = fetch_elevation(lat, lon)
    print("Elevation data received:")
    print(elev_data)
    print("-" * 50)

    print("4. Normalizing NASA + Open-Meteo data...")
    normalized = normalize_inputs(nasa_data, meteo_data)
    print("Normalized data keys:", normalized.keys())
    print("-" * 50)

    print("5. Building 14-feature row...")
    feature_row = build_feature_row(normalized, elev_data)
    print("Feature row:")
    print(feature_row)
    print("Feature count:", len(feature_row))
    print("-" * 50)

    if len(feature_row) == 14:
        print("SUCCESS: API + formatter pipeline is working.")
    else:
        print("ERROR: Feature row does not have 14 values.")

if __name__ == "__main__":
    test_all_apis()