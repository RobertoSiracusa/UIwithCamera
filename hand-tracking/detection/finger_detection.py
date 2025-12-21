"""
Finger detection functions for hand tracking.

Provides functions to detect if specific fingers are raised
based on MediaPipe hand landmark positions.
"""

from constants.landmarks import (
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
