# Hand Tracking Script

<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/db2ea975-e385-4ce9-8860-9a017f172ac3" />

A real-time hand tracking application using **MediaPipe** and **OpenCV** that detects hand landmarks and recognizes finger gestures. The script can detect when the **index finger** and **middle finger** are raised, displaying the status on screen in real-time.

## Features
- Real-time hand detection via webcam
- Draws 21 hand landmarks with connections
- Detects raised index finger
- Detects raised middle finger
- Visual feedback with color-coded status (green = raised, red = down)
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
pip install -r requirements.txt
```

---

## Run the Script

```bash
cd hand-tracking
python main.py
```

**To exit:** Close the window by clicking the X button.

---

## How It Works

### MediaPipe Hand Landmarks

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

A finger is considered **raised** when its tip (TIP) is positioned **higher** (lower Y value) than its base joints (PIP and MCP):

```python
is_raised = tip.y < pip.y and tip.y < mcp.y
```

---

## Project Structure

```
UIwithCamera/
├── hand-tracking/
│   └── main.py          # Main application script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

Enjoy!
