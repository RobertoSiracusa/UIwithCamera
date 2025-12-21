import cv2

import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe.python.solutions.drawing_styles as mp_drawing_styles


# Índices de los landmarks de cada dedo
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

# Diccionario con índices TIP de cada dedo para fácil acceso
FINGER_TIPS = {
    'thumb': THUMB_TIP,
    'index': INDEX_FINGER_TIP,
    'middle': MIDDLE_FINGER_TIP,
    'ring': RING_FINGER_TIP,
    'pinky': PINKY_TIP
}

def is_index_finger_raised(hand_landmarks):
    """
    Detecta si el dedo índice está levantado.
    
    Lógica: El dedo está levantado si la punta (TIP) está más arriba
    (menor valor Y) que las articulaciones PIP y MCP.
    
    Args:
        hand_landmarks: Landmarks de la mano detectada por MediaPipe.
    
    Returns:
        bool: True si el índice está levantado, False en caso contrario.
    """
    tip = hand_landmarks.landmark[INDEX_FINGER_TIP]
    pip = hand_landmarks.landmark[INDEX_FINGER_PIP]
    mcp = hand_landmarks.landmark[INDEX_FINGER_MCP]
    
    # En coordenadas de imagen, Y menor = más arriba en la pantalla
    # El dedo está levantado si la punta está por encima de PIP y MCP
    is_raised = tip.y < pip.y and tip.y < mcp.y
    
    return is_raised

def is_medium_finger_raised(hand_landmarks):
    tip = hand_landmarks.landmark[MIDDLE_FINGER_TIP]
    pip = hand_landmarks.landmark[MIDDLE_FINGER_PIP]
    mcp = hand_landmarks.landmark[MIDDLE_FINGER_MCP]

    is_raised = tip.y < pip.y and tip.y < mcp.y or tip.y < mcp.y
    return is_raised

def obtainFingerTipPosition(tip, height: int, width: int):
    """Convierte coordenadas normalizadas del landmark a píxeles."""
    tip_x = int(tip.x * width)
    tip_y = int(tip.y * height)
    return tip_x, tip_y


def draw_finger_rectangle(frame, hand_landmarks, finger_tip_index: int, 
                          height: int, width: int, color=(0, 255, 0), 
                          rect_size: int = 20, thickness: int = 2):
    """
    Dibuja un rectángulo centrado en la punta de un dedo especificado.
    
    Args:
        frame: Frame de video donde dibujar.
        hand_landmarks: Landmarks de la mano detectada por MediaPipe.
        finger_tip_index: Índice del landmark TIP del dedo (ej: INDEX_FINGER_TIP).
        height: Alto del frame en píxeles.
        width: Ancho del frame en píxeles.
        color: Color BGR del rectángulo. Default: verde (0, 255, 0).
        rect_size: Tamaño del rectángulo desde el centro. Default: 20.
        thickness: Grosor de la línea. Default: 2.
    """
    tip = hand_landmarks.landmark[finger_tip_index]
    tip_x, tip_y = obtainFingerTipPosition(tip, height, width)
    
    cv2.rectangle(
        frame,
        (tip_x - rect_size, tip_y - rect_size),
        (tip_x + rect_size, tip_y + rect_size),
        color,
        thickness
    )

def run_hand_tracking_on_webcam():
    
    cam = cv2.VideoCapture(index=0)

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        while cam.isOpened():
            success, frame = cam.read()
            if not success:
                print("Empty frame! Skipping.")
                continue

            # Aplicar efecto espejo al inicio
            frame = cv2.flip(frame, 1)
            
            height, width = frame.shape[:2]
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Detectar si el índice está levantado
                    index_raised = is_index_finger_raised(hand_landmarks)
                    medium_raised = is_medium_finger_raised(hand_landmarks)
                    
                    # Mostrar estado en pantalla
                    status_text = "INDICE LEVANTADO" if index_raised else "INDICE ABAJO"
                    color = (0, 255, 0) if index_raised else (0, 0, 255)
                    status_text2 = "MEDIO LEVANTADO" if medium_raised else "MEDIO ABAJO"
                    color2 = (0, 255, 0) if medium_raised else (0, 0, 255)
                    cv2.putText(
                        frame,
                        status_text,
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        color,
                        2,
                        cv2.LINE_AA
                    )
                    # poner texto en frame de camara
                    cv2.putText(
                        frame,
                        status_text2,
                        (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        color2,
                        2,
                        cv2.LINE_AA
                    )
                    # Dibujar rectángulos en las puntas de los 5 dedos
                    draw_finger_rectangle(frame, hand_landmarks, THUMB_TIP, height, width, color=(255, 0, 0))      # Azul
                    draw_finger_rectangle(frame, hand_landmarks, INDEX_FINGER_TIP, height, width, color=color)    # Color según estado
                    draw_finger_rectangle(frame, hand_landmarks, MIDDLE_FINGER_TIP, height, width, color=color2)  # Color según estado
                    draw_finger_rectangle(frame, hand_landmarks, RING_FINGER_TIP, height, width, color=(0, 255, 255))  # Amarillo
                    draw_finger_rectangle(frame, hand_landmarks, PINKY_TIP, height, width, color=(255, 0, 255))   # Magenta
                    
                    # Dibujar landmarks
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
                    )

            cv2.imshow("Hand Tracking", frame)
            cv2.waitKey(1)
            if cv2.getWindowProperty("Hand Tracking", cv2.WND_PROP_VISIBLE) < 1:
                break

    cam.release()

if __name__ == "__main__":
    run_hand_tracking_on_webcam()