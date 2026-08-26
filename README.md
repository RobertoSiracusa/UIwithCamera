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

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10 - 3.12 | 3.11 recommended |
| MediaPipe | `>=0.10.0, <0.11.0` | Classical solutions API compatibility |
| OpenCV | `>=4.8.0` | Video capture and UI rendering |
| Webcam | Required | Built-in or external USB |

---

## Installation by Operating System

### macOS (Apple Silicon & Intel)

```bash
# Clone or navigate to the project directory
cd UIwithCamera

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r hand-tracking/requirements.txt
```

### Fedora Linux / Red Hat / CentOS

```bash
# Ensure system prerequisites and video access (Fedora)
sudo dnf install -y python3-devel gcc

# Add user to video group for camera access (logout/login may be needed)
sudo usermod -aG video $USER

# Navigate to the project directory
cd UIwithCamera

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r hand-tracking/requirements.txt
```

### Windows (PowerShell / Command Prompt)

```powershell
# Navigate to the project directory
cd UIwithCamera

# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1
# Or in Command Prompt:
# venv\Scripts\activate.bat

# Install dependencies
pip install -r hand-tracking\requirements.txt
```

---

## Run the Application

You can run the application directly from the root project folder or from `hand-tracking/`:

```bash
# Run with default settings (camera index 0)
python hand-tracking/main.py

# Or from within the hand-tracking directory
cd hand-tracking
python main.py
```

### Optional Arguments

```bash
# Select a specific camera index (e.g., 1 for external USB webcam)
python hand-tracking/main.py --camera 1

# Change MediaPipe model complexity (0 = fastest/light, 1 = balanced, 2 = highest accuracy)
python hand-tracking/main.py --complexity 1

# Detect multiple hands
python hand-tracking/main.py --max-hands 2
```

### How to Exit

- Press **`q`** or **`ESC`** in the video window.
- Or close the window by clicking the **X** button.

---

## Troubleshooting & Permissions

- **macOS**: If camera access fails with `Error: No se pudo abrir la cámara`, open **System Settings > Privacy & Security > Camera** and enable permissions for your Terminal, iTerm, VS Code, or IDE.
- **Fedora / Linux**: If `/dev/video0` cannot be opened, verify that your user belongs to the `video` group (`groups $USER`) and check available devices (`ls -l /dev/video*`). If using Wayland or flatpak, ensure the terminal session has access to video devices.
- **Windows**: If the camera fails to initialize, go to **Settings > Privacy & Security > Camera** and make sure "Let desktop apps access your camera" is enabled.


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
