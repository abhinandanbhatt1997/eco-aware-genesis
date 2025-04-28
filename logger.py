from datetime import datetime

def log_decision(index):
    timestamp = datetime.utcnow().isoformat()
    with open("eco_log.txt", "a") as log_file:
        log_file.write(f"{timestamp}, Damage Index: {index:.4f}\n")
