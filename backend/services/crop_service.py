import pandas as pd
import os

# Path to your 10k-row knowledge base
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'advanced_agri_intelligence_10k.csv')

class CropService:
    def __init__(self):
        try:
            self.intel_base = pd.read_csv(DATA_PATH)
            print("✅ Crop Intelligence Service Initialized")
        except Exception as e:
            print(f"❌ Error loading Crop Intelligence: {e}")
            self.intel_base = None

    def get_prescriptive_data(self, crop_name):
        """
        Returns financial, seasonal, and mitigation data for a specific crop.
        """
        if self.intel_base is None:
            return {}

        try:
            # Case-insensitive match to find the first entry for this crop type
            row = self.intel_base[self.intel_base['suggested_crop'].str.lower() == crop_name.lower()].iloc[0]
            
            return {
                "market_price": int(row['market_price_msp']),
                "est_cost": int(row['cultivation_cost_per_hectare']),
                "season": row['planting_window'],
                "soil_ph": row['ph_requirement'],
                "mitigation": {
                    "drought": row['drought_mitigation_strategy'],
                    "waterlogging": row['waterlogging_mitigation_strategy'],
                    "erosion": row['erosion_mitigation_strategy'],
                    "frost": row['frost_mitigation_strategy']
                }
            }
        except Exception as e:
            print(f"Metadata lookup failed for {crop_name}: {e}")
            return {
                "market_price": 2500,
                "season": "Year-round",
                "mitigation": {"drought": "Monitor soil moisture.", "waterlogging": "Check drainage."}
            }