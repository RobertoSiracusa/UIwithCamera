"""
Hand Tracking Application

Real-time hand tracking using MediaPipe and OpenCV.
Detects finger gestures and displays visual feedback.
"""

import sys
from pathlib import Path

# Add package directory to sys.path so it can be executed from any working directory
PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from core.hand_tracker import HandTracker


if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()