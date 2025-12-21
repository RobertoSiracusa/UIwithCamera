"""
Hand Tracking Application

Real-time hand tracking using MediaPipe and OpenCV.
Detects finger gestures and displays visual feedback.
"""

from core.hand_tracker import HandTracker


if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()