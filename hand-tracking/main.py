import cv2

import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe.python.solutions.drawing_styles as mp_drawing_styles


# Índices de los landmarks del dedo índice
INDEX_FINGER_TIP = 8   # Punta del índice
INDEX_FINGER_DIP = 7   # Articulación distal
INDEX_FINGER_PIP = 6   # Articulación proximal
INDEX_FINGER_MCP = 5   # Nudillo (base del dedo)


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
                    
                    # Mostrar estado en pantalla
                    status_text = "INDICE LEVANTADO" if index_raised else "INDICE ABAJO"
                    color = (0, 255, 0) if index_raised else (0, 0, 255)
                    
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