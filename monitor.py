import random
import requests
import os

def get_damage_index():
    """
    Fetch real carbon intensity from electricityMap API.
    Falls back to simulated index if API fails or not set.
    """
    token = os.getenv("ELECTRICITY_MAP_TOKEN")
    zone = os.getenv("CARBON_ZONE", "DE")  # Default to Germany
    if token:
        try:
            response = requests.get(
                f"https://api.electricitymap.org/v3/carbon-intensity/latest?zone={zone}",
                headers={"auth-token": token}
            )
            response.raise_for_status()
            data = response.json()
            gco2_per_kwh = data['carbonIntensity']['gCO2eqPerkWh']
            return normalize_carbon(gco2_per_kwh)
        except Exception as e:
            print(f"[⚠️] Failed to fetch carbon intensity: {e}")
    return random.uniform(0, 1)

def normalize_carbon(value, min_val=0, max_val=800):
    """
    Normalize CO2 g/kWh to a 0–1 range.
    """
    return max(0, min(1, (value - min_val) / (max_val - min_val)))
