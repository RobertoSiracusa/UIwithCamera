# Hand Tracking Application

<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/db2ea975-e385-4ce9-8860-9a017f172ac3" />

A real-time hand tracking application using MediaPipe and OpenCV that detects hand landmarks and recognizes finger gestures. The script detects when fingers are raised, displaying status on screen in real-time with color-coded visual feedback.

## Features

- Real-time hand detection via webcam
- Draws 21 hand landmarks with connections
- Detects raised fingers (index and middle)
- Visual feedback with color-coded rectangles on each fingertip
- Status text display (green = raised, red = down)
- Mirror effect for natural interaction

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| MediaPipe | Latest |
| OpenCV | Latest |
| Webcam | Required |

### Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r hand-tracking/requirements.txt
```

---

## Run the Application

```bash
cd hand-tracking
python main.py
```

To exit: Close the window by clicking the X button.

---

## Project Architecture

The project follows a modular top-down design pattern with clear separation of concerns:

```
hand-tracking/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── constants/
│   ├── __init__.py
│   └── landmarks.py             # Finger landmark indices (0-20)
├── detection/
│   ├── __init__.py
│   └── finger_detection.py      # Finger raised detection logic
├── visualization/
│   ├── __init__.py
│   └── drawing.py               # Drawing utilities (rectangles, text)
└── core/
    ├── __init__.py
    └── hand_tracker.py          # Main HandTracker class
```

### Module Descriptions

| Module | Purpose |
|--------|---------|
| constants | Landmark indices for all 21 hand points, organized by finger |
| detection | Functions to detect if fingers are raised based on landmark positions |
| visualization | Drawing utilities for rectangles and status text on video frames |
| core | Main HandTracker class with webcam capture and processing loop |

---

## MediaPipe Hand Landmarks

Each hand has 21 landmarks numbered 0-20:

```
        THUMB     INDEX     MIDDLE    RING      PINKY
TIP       4         8        12        16        20
DIP       3         7        11        15        19
PIP       2         6        10        14        18
MCP       1         5         9        13        17
WRIST                        0
```

### Finger Detection Logic

A finger is considered raised when its tip (TIP) is positioned higher (lower Y value in image coordinates) than its base joints (PIP and MCP):

```python
is_raised = tip.y < pip.y and tip.y < mcp.y
```

---

## Extending the Application

### Adding detection for more fingers

Use the generic `is_finger_raised()` function in `detection/finger_detection.py`:

```python
from constants.landmarks import RING_FINGER_TIP, RING_FINGER_PIP, RING_FINGER_MCP
from detection.finger_detection import is_finger_raised

ring_raised = is_finger_raised(
    hand_landmarks, 
    RING_FINGER_TIP, 
    RING_FINGER_PIP, 
    RING_FINGER_MCP
)
```

### Customizing the HandTracker

```python
from core.hand_tracker import HandTracker

tracker = HandTracker(
    camera_index=0,
    model_complexity=1,        # 0, 1, or 2 (higher = more accurate, slower)
    max_num_hands=2,           # Detect up to 2 hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
tracker.run()
```

---

## License

MIT License
