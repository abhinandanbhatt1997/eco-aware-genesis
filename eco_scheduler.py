# main.py
import argparse
from eco_core.eco_agent import EcoAwareAgent
from utils.visualizer import plot_log
from eco_core.eco_scheduler import run_when_green

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Eco-Aware AI Runner")
    parser.add_argument("--force", action="store_true", help="Force computation regardless of eco damage")
    parser.add_argument("--threshold", type=float, default=0.3, help="Set custom eco-damage threshold (0-1)")
    parser.add_argument("--plot", action="store_true", help="Plot eco-damage history")
    parser.add_argument("--wait", action="store_true", help="Wait until eco damage is low before running")
    args = parser.parse_args()

    if args.plot:
        plot_log()
    elif args.wait:
        run_when_green(threshold=args.threshold)
    else:
        agent = EcoAwareAgent(eco_threshold=args.threshold)
        agent.maybe_compute(force=args.force)


# eco_core/eco_agent.py
from eco_core.monitor import get_damage_index
from eco_core.scheduler import should_compute
from models.run_model import run_model
from utils.logger import log_decision

class EcoAwareAgent:
    def __init__(self, eco_threshold=0.3):
        self.threshold = eco_threshold

    def maybe_compute(self, force=False):
        index = get_damage_index()
        log_decision(index)
        print(f"[🌍] Current Damage Index: {index:.2f}")
        if force or should_compute(index, self.threshold):
            print("[✅] Green condition met. Running task...")
            run_model()
        else:
            print("[🌱] Too much damage. Waiting for better conditions.")


# eco_core/monitor.py
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


# eco_core/scheduler.py
def should_compute(damage_index, threshold=0.3):
    return damage_index < threshold


# eco_core/eco_scheduler.py
import time
from eco_core.monitor import get_damage_index
from models.run_model import run_model
from utils.logger import log_decision
from eco_core.scheduler import should_compute

def run_when_green(threshold=0.3, check_interval=60):
    print("[⏳] Waiting for eco-friendly conditions...")
    while True:
        index = get_damage_index()
        log_decision(index)
        print(f"[🌍] Current Damage Index: {index:.2f}")
        if should_compute(index, threshold):
            print("[✅] Conditions met. Executing task!")
            run_model()
            break
        else:
            print(f"[🌱] Still too high. Checking again in {check_interval}s...")
            time.sleep(check_interval)


# models/run_model.py
def run_model():
    print("[⚙️] Running eco-aware model task...")
    total = sum(i ** 2 for i in range(1000000))
    print(f"[✔️] Task complete. Result: {total}")


# utils/logger.py
from datetime import datetime

def log_decision(index):
    timestamp = datetime.utcnow().isoformat()
    with open("eco_log.txt", "a") as log_file:
        log_file.write(f"{timestamp}, Damage Index: {index:.4f}\n")


# utils/visualizer.py
import matplotlib.pyplot as plt
import datetime

def plot_log(log_path="eco_log.txt"):
    timestamps, values = [], []
    try:
        with open(log_path, "r") as f:
            for line in f:
                time_str, value_str = line.strip().split(", Damage Index: ")
                timestamps.append(datetime.datetime.fromisoformat(time_str))
                values.append(float(value_str))

        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, values, marker='o', linestyle='-', color='green')
        plt.xlabel("Timestamp")
        plt.ylabel("Damage Index")
        plt.title("Eco Damage Over Time")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[❌] Failed to visualize logs: {e}")
