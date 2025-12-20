# Hand Tracking Script - Script de Detector de Manos 

<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/db2ea975-e385-4ce9-8860-9a017f172ac3" />
## English

A real-time hand tracking application using **MediaPipe** and **OpenCV** that detects hand landmarks and recognizes finger gestures. The script can detect when the **index finger** and **middle finger** are raised, displaying the status on screen in real-time.

### Features
- Real-time hand detection via webcam
- Draws 21 hand landmarks with connections
- Detects raised index finger (dedo índice)
- Detects raised middle finger (dedo medio)
- Visual feedback with color-coded status (green = raised, red = down)
- Mirror effect for natural interaction

---

## Español

Una aplicación de detección de manos en tiempo real usando **MediaPipe** y **OpenCV** que detecta los puntos de referencia de la mano y reconoce gestos de los dedos. El script puede detectar cuándo el **dedo índice** y el **dedo medio** están levantados, mostrando el estado en pantalla en tiempo real.

### Características
- Detección de manos en tiempo real con la webcam
- Dibuja 21 landmarks de la mano con sus conexiones
- Detecta si el dedo índice está levantado
- Detecta si el dedo medio está levantado
- Retroalimentación visual con colores (verde = levantado, rojo = abajo)
- Efecto espejo para una interacción natural

---

## Requirements - Requerimientos

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| MediaPipe | Latest |
| OpenCV | Latest |
| Webcam | Required |

### Installation - Instalación

```bash
# Create virtual environment | Crear entorno virtual
python3 -m venv venv

# Activate | Activar
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies | Instalar dependencias
pip install -r requirements.txt
```

---

## Run the Script - Ejecutar el Script

```bash
cd hand-tracking
python main.py
```

**To exit | Para salir:** Close the window by clicking the X button.

---

## How It Works - Cómo Funciona

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

## Project Structure - Estructura del Proyecto

```
UIwithCamera/
├── hand-tracking/
│   └── main.py          # Main application script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

Enjoy! | ¡Que te diviertas! 
