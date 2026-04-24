from flask import Flask, jsonify, request
from flask_cors import CORS

from services.nasa_power import fetch_nasa_power
from services.open_meteo import fetch_open_meteo
from services.elevation import fetch_elevation
from services.formatter import normalize_inputs, build_feature_row
from engine.risk_engine import generate_risks

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Agri-Risk AI Fusion API is Online"

@app.route("/predict", methods=["GET"])
def predict():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))

        nasa_data = fetch_nasa_power(lat, lon)
        meteo_data = fetch_open_meteo(lat, lon)
        elev_data = fetch_elevation(lat, lon)

        normalized = normalize_inputs(nasa_data, meteo_data)
        feature_row = build_feature_row(normalized, elev_data)

        risks = generate_risks(feature_row)

        return jsonify({
            "location": {
                "lat": lat,
                "lon": lon
            },
            "nasa_data": nasa_data,
            "meteo_data": meteo_data,
            "elevation_data": elev_data,
            "normalized_data": normalized,
            "features_used": feature_row,
            "risks": risks
        })

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    