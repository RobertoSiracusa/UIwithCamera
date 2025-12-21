"""
Drawing utilities for hand tracking visualization.

Provides functions to draw rectangles, text, and other
visual elements on video frames.
"""

import cv2
from typing import Tuple


def get_pixel_position(landmark, height: int, width: int) -> Tuple[int, int]:
    """
    Converts normalized landmark coordinates to pixel coordinates.
    
    Args:
        landmark: MediaPipe landmark with x, y attributes (normalized 0-1).
        height: Frame height in pixels.
        width: Frame width in pixels.
    
    Returns:
        Tuple[int, int]: (x, y) pixel coordinates.
    """
    x = int(landmark.x * width)
    y = int(landmark.y * height)
    return x, y


def draw_finger_rectangle(frame, hand_landmarks, finger_tip_index: int,
                          height: int, width: int,
                          color: Tuple[int, int, int] = (0, 255, 0),
                          rect_size: int = 20,
                          thickness: int = 2) -> None:
    """
    Draws a rectangle centered on the specified fingertip.
    
    Args:
        frame: Video frame to draw on.
        hand_landmarks: Hand landmarks detected by MediaPipe.
        finger_tip_index: Index of the fingertip landmark.
        height: Frame height in pixels.
        width: Frame width in pixels.
        color: BGR color tuple. Default: green (0, 255, 0).
        rect_size: Half-size of the rectangle. Default: 20px.
        thickness: Line thickness. Default: 2px.
    """
    tip = hand_landmarks.landmark[finger_tip_index]
    tip_x, tip_y = get_pixel_position(tip, height, width)
    
    cv2.rectangle(
        frame,
        (tip_x - rect_size, tip_y - rect_size),
        (tip_x + rect_size, tip_y + rect_size),
        color,
        thickness
    )


def draw_status_text(frame, text: str, position: Tuple[int, int],
                     color: Tuple[int, int, int],
                     font_scale: float = 1,
                     thickness: int = 2) -> None:
    """
    Draws status text on the frame.
    
    Args:
        frame: Video frame to draw on.
        text: Text string to display.
        position: (x, y) position for the text.
        color: BGR color tuple.
        font_scale: Font scale factor. Default: 1.
        thickness: Text thickness. Default: 2.
    """
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA
    )
