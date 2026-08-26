"""
Hand Tracker - Main tracking loop and application logic.

Provides the HandTracker class that manages webcam capture,
hand detection, and visualization.
"""

import cv2
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe.python.solutions.drawing_styles as mp_drawing_styles

from constants.landmarks import (
    THUMB_TIP, INDEX_FINGER_TIP, MIDDLE_FINGER_TIP,
    RING_FINGER_TIP, PINKY_TIP
)
from detection.finger_detection import is_index_finger_raised, is_middle_finger_raised, is_thumb_raised, get_pinch_level
from visualization.drawing import draw_finger_rectangle, draw_status_text, draw_pinch_status, draw_pinch_line


class HandTracker:
    """
    Real-time hand tracking application.
    
    Captures video from webcam, detects hands using MediaPipe,
    and displays finger status with visual feedback.
    """
    
    def __init__(self, camera_index: int = 0,
                 model_complexity: int = 0,
                 max_num_hands: int = 1,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the hand tracker.
        
        Args:
            camera_index: Webcam index. Default: 0.
            model_complexity: MediaPipe model complexity (0-2). Default: 0.
            max_num_hands: Maximum hands to detect. Default: 1.
            min_detection_confidence: Detection threshold. Default: 0.5.
            min_tracking_confidence: Tracking threshold. Default: 0.5.
        """
        self.camera_index = camera_index
        self.model_complexity = model_complexity
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.window_name = "Hand Tracking"
    
    def _print_camera_troubleshooting(self) -> None:
        """Prints OS-specific camera troubleshooting hints."""
        import sys
        print(f"Error: No se pudo abrir la cámara con índice {self.camera_index}.")
        if sys.platform == "darwin":
            print("Sugerencia (macOS): Verifica los permisos en 'Ajustes del Sistema > Privacidad y Seguridad > Cámara'.")
        elif sys.platform.startswith("linux"):
            print("Sugerencia (Linux/Fedora): Verifica permisos en el grupo de video:")
            print("  sudo usermod -aG video $USER")
            print("y confirma que el dispositivo existe (ej: /dev/video0 o /dev/video1).")
        elif sys.platform == "win32":
            print("Sugerencia (Windows): Verifica permisos en 'Configuración > Privacidad y seguridad > Cámara'.")
        else:
            print("Verifica que la cámara esté conectada y no esté siendo usada por otra aplicación.")

    def run(self) -> None:
        """Main tracking loop. Captures frames and processes hands."""
        cam = cv2.VideoCapture(index=self.camera_index)
        if not cam.isOpened():
            self._print_camera_troubleshooting()
            return
        
        try:
            with mp_hands.Hands(
                model_complexity=self.model_complexity,
                max_num_hands=self.max_num_hands,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            ) as hands:
                while cam.isOpened():
                    success, frame = cam.read()
                    if not success:
                        print("Empty frame! Skipping.")
                        continue
                    
                    # Apply mirror effect
                    frame = cv2.flip(frame, 1)
                    
                    # Process frame
                    self._process_frame(frame, hands)
                    
                    # Display frame
                    cv2.imshow(self.window_name, frame)
                    
                    # Handle key presses ('q' or ESC to exit)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q') or key == 27:
                        break
                    
                    # Handle window close button safely across OS backends
                    try:
                        if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                            break
                    except Exception:
                        pass
        finally:
            cam.release()
            cv2.destroyAllWindows()


    
    def _process_frame(self, frame, hands) -> None:
        """
        Process a single frame for hand detection.
        
        Args:
            frame: BGR video frame to process.
            hands: MediaPipe Hands object.
        """
        height, width = frame.shape[:2]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if not results.multi_hand_landmarks:
            return
        
        for hand_landmarks in results.multi_hand_landmarks:
            # Detect finger states
            index_raised = is_index_finger_raised(hand_landmarks)
            middle_raised = is_middle_finger_raised(hand_landmarks)
            thumb_raised = is_thumb_raised(hand_landmarks)
            # Determine colors and status
            index_color = (0, 255, 0) if index_raised else (0, 0, 255)
            middle_color = (0, 255, 0) if middle_raised else (0, 0, 255)
            thumb_color = (0, 255, 0) if thumb_raised else (0, 0, 255)
            index_text = "INDICE LEVANTADO" if index_raised else "INDICE ABAJO"
            middle_text = "MEDIO LEVANTADO" if middle_raised else "MEDIO ABAJO"
            thumb_text = "PULGAR LEVANTADO" if thumb_raised else "PULGAR ABAJO"
            draw_status_text(frame, index_text, (10, 40), index_color)
            draw_status_text(frame, middle_text, (10, 80), middle_color)
            draw_status_text(frame, thumb_text, (10, 120), thumb_color)
            
            # Draw pinch status
            pinch_level = get_pinch_level(hand_landmarks, height, width)
            draw_pinch_status(frame, pinch_level)
            
            # Draw line between thumb and index tips
            draw_pinch_line(frame, hand_landmarks, height, width, THUMB_TIP, INDEX_FINGER_TIP)
            
            # Draw rectangles on all fingertips
            draw_finger_rectangle(frame, hand_landmarks, THUMB_TIP, height, width, color=thumb_color)
            draw_finger_rectangle(frame, hand_landmarks, INDEX_FINGER_TIP, height, width, color=index_color)
            draw_finger_rectangle(frame, hand_landmarks, MIDDLE_FINGER_TIP, height, width, color=middle_color)
            draw_finger_rectangle(frame, hand_landmarks, RING_FINGER_TIP, height, width, color=(0, 255, 255))
            draw_finger_rectangle(frame, hand_landmarks, PINKY_TIP, height, width, color=(255, 0, 255))
            
            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=hand_landmarks,
                connections=mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
            )
