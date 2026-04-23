import joblib
import os

# This tells Python to look in the same folder where this script is saved
current_dir = os.path.dirname(os.path.abspath(__file__))

model_files = [
    'waterlogging_risk.pkl', 
    'drought_risk.pkl', 
    'frost_risk.pkl', 
    'erosion_risk.pkl',
    'train_stats.pkl'
]

print("\n--- 🛡️ Model Integrity Check ---")
print(f"Checking directory: {current_dir}\n")

for file in model_files:
    path = os.path.join(current_dir, file) 
    if os.path.exists(path):
        try:
            loaded_data = joblib.load(path)
            print(f"✅ {file}: Loaded successfully!")
        except Exception as e:
            print(f"❌ {file}: Error loading! ({e})")
    else:
        print(f"⚠️ {file}: File not found! Expected at: {path}")

print("\n--------------------------------")