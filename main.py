# main.py
import argparse
from eco_core.eco_agent import EcoAwareAgent  # <-- Fixed
from utils.visualizer import plot_log

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Eco-Aware AI Runner")
    parser.add_argument("--force", action="store_true", help="Force computation regardless of eco damage")
    parser.add_argument("--threshold", type=float, default=0.3, help="Set custom eco-damage threshold (0-1)")
    parser.add_argument("--plot", action="store_true", help="Plot eco-damage history")
    args = parser.parse_args()

    if args.plot:
        plot_log()
    else:
        agent = EcoAwareAgent(eco_threshold=args.threshold)
        agent.maybe_compute(force=args.force)
