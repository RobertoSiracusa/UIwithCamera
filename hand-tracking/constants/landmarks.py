"""
Landmark indices for MediaPipe hand tracking.

Each hand has 21 landmarks numbered 0-20.
The landmark hierarchy for each finger (except thumb):
    TIP -> DIP -> PIP -> MCP

For thumb:
    TIP -> IP -> MCP -> CMC
"""

# WRIST
WRIST = 0

# PULGAR (Thumb)
THUMB_TIP = 4
THUMB_IP = 3
THUMB_MCP = 2
THUMB_CMC = 1

# ÍNDICE (Index)
INDEX_FINGER_TIP = 8
INDEX_FINGER_DIP = 7
INDEX_FINGER_PIP = 6
INDEX_FINGER_MCP = 5

# MEDIO (Middle)
MIDDLE_FINGER_TIP = 12
MIDDLE_FINGER_DIP = 11
MIDDLE_FINGER_PIP = 10
MIDDLE_FINGER_MCP = 9

# ANULAR (Ring)
RING_FINGER_TIP = 16
RING_FINGER_DIP = 15
RING_FINGER_PIP = 14
RING_FINGER_MCP = 13

# MEÑIQUE (Pinky)
PINKY_TIP = 20
PINKY_DIP = 19
PINKY_PIP = 18
PINKY_MCP = 17

# Dictionary for easy access to finger tip indices
FINGER_TIPS = {
    'thumb': THUMB_TIP,
    'index': INDEX_FINGER_TIP,
    'middle': MIDDLE_FINGER_TIP,
    'ring': RING_FINGER_TIP,
    'pinky': PINKY_TIP
}

# Finger landmark sets (TIP, DIP/IP, PIP/MCP, MCP/CMC)
FINGER_LANDMARKS = {
    'thumb': (THUMB_TIP, THUMB_IP, THUMB_MCP, THUMB_CMC),
    'index': (INDEX_FINGER_TIP, INDEX_FINGER_DIP, INDEX_FINGER_PIP, INDEX_FINGER_MCP),
    'middle': (MIDDLE_FINGER_TIP, MIDDLE_FINGER_DIP, MIDDLE_FINGER_PIP, MIDDLE_FINGER_MCP),
    'ring': (RING_FINGER_TIP, RING_FINGER_DIP, RING_FINGER_PIP, RING_FINGER_MCP),
    'pinky': (PINKY_TIP, PINKY_DIP, PINKY_PIP, PINKY_MCP)
}
