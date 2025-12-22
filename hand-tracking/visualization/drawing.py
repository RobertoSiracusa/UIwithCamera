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


def draw_pinch_status(frame, pinch_level: int, position: tuple = (10, 160),
                      font_scale: float = 1, thickness: int = 2) -> None:
    """
    Draws pinch status text based on the pinch level (0-3).
    
    Args:
        frame: Video frame to draw on.
        pinch_level: Level from 0-3 (0=closed, 3=open).
        position: (x, y) position for the text.
        font_scale: Font scale factor. Default: 1.
        thickness: Text thickness. Default: 2.
    """
    # Map level to text and color
    status_map = {
        0: ("PINCH: CERRADO", (255, 0, 0)),    # Blue - closed
        1: ("PINCH: CERCA", (0, 165, 255)),    # Orange
        2: ("PINCH: MEDIO", (0, 255, 255)),    # Yellow
        3: ("PINCH: ABIERTO", (0, 255, 0))     # Green - open
    }
    
    text, color = status_map.get(pinch_level, ("PINCH: ???", (255, 255, 255)))
    
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


def draw_pinch_line(frame, hand_landmarks, height: int, width: int,
                    thumb_tip_idx: int, index_tip_idx: int) -> None:
    """
    Draws a line between thumb tip and index tip.
    Color and thickness vary based on distance (pinch level).
    
    Args:
        frame: Video frame to draw on.
        hand_landmarks: Hand landmarks from MediaPipe.
        height: Frame height in pixels.
        width: Frame width in pixels.
        thumb_tip_idx: Landmark index for thumb tip.
        index_tip_idx: Landmark index for index finger tip.
    """
    import math
    
    thumb = hand_landmarks.landmark[thumb_tip_idx]
    index = hand_landmarks.landmark[index_tip_idx]
    
    # Convert to pixel coordinates
    thumb_pos = (int(thumb.x * width), int(thumb.y * height))
    index_pos = (int(index.x * width), int(index.y * height))
    
    # Calculate distance for color/thickness
    dx = thumb_pos[0] - index_pos[0]
    dy = thumb_pos[1] - index_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    # Map distance to color and thickness
    if distance < 30:
        color = (255, 0, 0)      # Blue - closed
        thickness = 6
    elif distance < 60:
        color = (0, 165, 255)    # Orange
        thickness = 5
    elif distance < 100:
        color = (0, 255, 255)    # Yellow
        thickness = 4
    else:
        color = (0, 255, 0)      # Green - open
        thickness = 3
    
    cv2.line(frame, thumb_pos, index_pos, color, thickness)

