import requests
import json

# Replace with your local URL or ngrok URL
URL = "http://127.0.0.1:5000/predict"
PARAMS = {
    "lat": 12.9716,  # Example: Bangalore area
    "lon": 77.5946
}

print("🚀 Sending request to Agri-Risk API...")
response = requests.get(URL, params=PARAMS)

if response.status_code == 200:
    data = response.json()
    print("\n✅ API Response Received!")
    print(f"Suggested Crop: {data['recommendation']['crop']}")
    print(f"Market Price (MSP): ₹{data['recommendation']['msp']}")
    print(f"Season: {data['recommendation']['season']}")
    print("-" * 30)
    print("Risk Assessment:")
    for risk, details in data['risks'].items():
        print(f" - {risk.upper()}: {details['level']} ({details['confidence']})")
    print("-" * 30)
    print("Action Plan (Prescriptive):")
    # This proves your 10k-row CSV lookup is working!
    print(f"DRY SPELL ACTION: {data['mitigation_strategies']['drought']}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)