"""
Hand Tracking Application

Real-time hand tracking using MediaPipe and OpenCV.
Detects finger gestures and displays visual feedback.
"""

import argparse
import sys
from pathlib import Path

# Add package directory to sys.path so it can be executed from any working directory
PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from core.hand_tracker import HandTracker


def parse_args():
    parser = argparse.ArgumentParser(description="Hand Tracking Application")
    parser.add_argument("--camera", type=int, default=0, help="Webcam device index (default: 0)")
    parser.add_argument("--complexity", type=int, default=0, choices=[0, 1, 2], help="MediaPipe model complexity 0-2 (default: 0)")
    parser.add_argument("--max-hands", type=int, default=1, help="Max hands to detect (default: 1)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    tracker = HandTracker(
        camera_index=args.camera,
        model_complexity=args.complexity,
        max_num_hands=args.max_hands,
    )
    tracker.run()