"""
Finger detection functions for hand tracking.

Provides functions to detect if specific fingers are raised
based on MediaPipe hand landmark positions.
"""

import math

from constants.landmarks import (
    THUMB_TIP, THUMB_IP, THUMB_MCP,
    INDEX_FINGER_TIP, INDEX_FINGER_PIP, INDEX_FINGER_MCP,
    MIDDLE_FINGER_TIP, MIDDLE_FINGER_PIP, MIDDLE_FINGER_MCP
)


def is_finger_raised(hand_landmarks, tip_idx: int, pip_idx: int, mcp_idx: int) -> bool:
    """
    Generic function to detect if a finger is raised.
    
    Logic: A finger is considered raised if its tip (TIP) is positioned
    higher (lower Y value) than its PIP and MCP joints.
    
    Args:
        hand_landmarks: Landmarks detected by MediaPipe.
        tip_idx: Index of the fingertip landmark.
        pip_idx: Index of the PIP joint landmark.
        mcp_idx: Index of the MCP joint landmark.
    
    Returns:
        bool: True if the finger is raised, False otherwise.
    """
    tip = hand_landmarks.landmark[tip_idx]
    pip = hand_landmarks.landmark[pip_idx]
    mcp = hand_landmarks.landmark[mcp_idx]
    
    # In image coordinates, lower Y = higher on screen
    return tip.y < pip.y and tip.y < mcp.y


def is_index_finger_raised(hand_landmarks) -> bool:
    """
    Detects if the index finger is raised.
    
    Args:
        hand_landmarks: Landmarks detected by MediaPipe.
    
    Returns:
        bool: True if the index finger is raised.
    """
    return is_finger_raised(
        hand_landmarks,
        INDEX_FINGER_TIP,
        INDEX_FINGER_PIP,
        INDEX_FINGER_MCP
    )


def is_thumb_raised(hand_landmarks) -> bool:
    """
    Detects if the thumb is raised/extended.
    
    Note: Thumb detection uses X-axis instead of Y-axis since
    the thumb moves horizontally relative to the palm.
    
    Args:
        hand_landmarks: Landmarks detected by MediaPipe.
    
    Returns:
        bool: True if the thumb is extended.
    """
    tip = hand_landmarks.landmark[THUMB_TIP]
    ip = hand_landmarks.landmark[THUMB_IP]
    mcp = hand_landmarks.landmark[THUMB_MCP]
    
    # Thumb extends outward (X-axis) more than vertically
    # Check if tip is further from palm center than other joints
    return tip.x < ip.x and tip.x < mcp.x


def is_middle_finger_raised(hand_landmarks) -> bool:
    """
    Detects if the middle finger is raised.
    
    Args:
        hand_landmarks: Landmarks detected by MediaPipe.
    
    Returns:
        bool: True if the middle finger is raised.
    """
    return is_finger_raised(
        hand_landmarks,
        MIDDLE_FINGER_TIP,
        MIDDLE_FINGER_PIP,
        MIDDLE_FINGER_MCP
    )


def get_pinch_level(hand_landmarks, height: int, width: int) -> int:
    """
    Returns a level 0-3 based on thumb-index finger distance.
    
    Levels:
        0 = Very close (pinch closed)
        1 = Close
        2 = Medium
        3 = Far (open)
    
    Args:
        hand_landmarks: Landmarks detected by MediaPipe.
        height: Frame height in pixels.
        width: Frame width in pixels.
    
    Returns:
        int: Pinch level from 0 (closed) to 3 (open).
    """
    thumb_tip = hand_landmarks.landmark[THUMB_TIP]
    index_tip = hand_landmarks.landmark[INDEX_FINGER_TIP]
    
    # Calculate euclidean distance (scale to pixels)
    dx = (thumb_tip.x - index_tip.x) * width
    dy = (thumb_tip.y - index_tip.y) * height
    distance = math.sqrt(dx**2 + dy**2)
    
    # Map distance to levels (adjust thresholds as needed)
    if distance < 30:
        return 0  # Pinch closed
    elif distance < 60:
        return 1  # Close
    elif distance < 100:
        return 2  # Medium
    else:
        return 3  # Open
