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

