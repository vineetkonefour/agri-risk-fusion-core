from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

# Import your custom services
from services.nasa_power import fetch_nasa_power
from services.open_meteo import fetch_open_meteo
from services.elevation import fetch_elevation
from services.formatter import normalize_inputs, build_feature_row
from engine.risk_engine import generate_risks

app = Flask(__name__)

# PRECAUTION 1: Enable CORS so Lovable can talk to your local Flask/Ngrok server
CORS(app)

# PRECAUTION 2: Load the Intelligence Base once when the server starts for speed
# Ensure the file is in 'backend/data/advanced_agri_intelligence_10k.csv'
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'advanced_agri_intelligence_10k.csv')

try:
    intel_base = pd.read_csv(DATA_PATH)
    print("✅ Intelligence Base Loaded Successfully")
except Exception as e:
    print(f"❌ Error Loading Intelligence Base: {e}")
    intel_base = None

def get_crop_metadata(crop_name):
    """
    Looks up the prescriptive metadata (MSP, Mitigation, Season) for a given crop.
    """
    if intel_base is None:
        return {}
    
    try:
        # Match the crop name (case-insensitive)
        row = intel_base[intel_base['suggested_crop'].str.lower() == crop_name.lower()].iloc[0]
        return {
            "msp": int(row['market_price_msp']),
            "cultivation_cost": int(row['cultivation_cost_per_hectare']),
            "season": row['planting_window'],
            "ph_pref": row['ph_requirement'],
            "mitigation": {
                "drought": row['drought_mitigation_strategy'],
                "waterlogging": row['waterlogging_mitigation_strategy'],
                "erosion": row['erosion_mitigation_strategy'],
                "frost": row['frost_mitigation_strategy']
            }
        }
    except IndexError:
        return {"error": "Crop metadata not found."}

@app.route("/")
def home():
    return "Agri-Risk AI Fusion API is Online. Send GET requests to /predict?lat=...&lon=..."

@app.route("/predict", methods=["GET"])
def predict():
    try:
        # 1. Extract and Validate Coordinates
        lat_raw = request.args.get("lat")
        lon_raw = request.args.get("lon")
        
        if not lat_raw or not lon_raw:
            return jsonify({"error": "Missing latitude (lat) or longitude (lon) parameters"}), 400
            
        lat = float(lat_raw)
        lon = float(lon_raw)

        # 2. Fetch Real-time Environmental Data
        nasa_data = fetch_nasa_power(lat, lon)
        meteo_data = fetch_open_meteo(lat, lon)
        elev_data = fetch_elevation(lat, lon)

        # 3. Format into the 14-Feature Environmental DNA
        normalized = normalize_inputs(nasa_data, meteo_data)
        feature_row = build_feature_row(normalized, elev_data)

        # 4. Run the 5 XGBoost Models (4 Risk + 1 Crop)
        # Note: generate_risks must return a dict with risk levels and 'suggested_crop'
        predictions = generate_risks(feature_row)
        
        # 5. The Prescriptive Lookup (Metadata)
        suggested_crop = predictions.get("suggested_crop", "Rice")
        metadata = get_crop_metadata(suggested_crop)

        # 6. Final Structured Response for Frontend
        return jsonify({
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "recommendation": {
                "crop": suggested_crop,
                "msp": metadata.get("msp"),
                "cost": metadata.get("cultivation_cost"),
                "season": metadata.get("season"),
                "ph": metadata.get("ph_pref")
            },
            "risks": predictions.get("risks"),
            "mitigation_strategies": metadata.get("mitigation"),
            "raw_diagnostics": {
                "elevation": elev_data,
                "weather": normalized
            }
        })

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure port 5000 is open for ngrok to tunnel
    app.run(host="0.0.0.0", port=5000, debug=True)