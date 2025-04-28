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

