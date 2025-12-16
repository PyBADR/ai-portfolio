"""
Hand Tracking Module
Uses OpenCV for hand detection with simulated gesture recognition
Note: MediaPipe is not available on Apple Silicon, so this uses a demo mode
"""

from typing import Tuple, Optional, Any
import cv2  # type: ignore
import numpy as np  # type: ignore
import time


class HandTracker:
    def __init__(self) -> None:
        self.demo_mode = False  # Enable real camera mode
        self.gesture_cycle = ['open', 'closed', 'swipe_left', 'swipe_right']
        self.current_gesture_idx = 0
        self.last_gesture_change = time.time()
        self.gesture_duration = 4  # Change gesture every 4 seconds in demo mode
        
    def process_frame(self, frame: Any) -> Tuple[Any, Optional[Any], str]:
        """
        Process a frame and return hand landmarks
        Returns: (processed_frame, landmarks, hand_state)
        """
        # In demo mode, cycle through gestures automatically
        if self.demo_mode:
            current_time = time.time()
            if current_time - self.last_gesture_change > self.gesture_duration:
                self.current_gesture_idx = (self.current_gesture_idx + 1) % len(self.gesture_cycle)
                self.last_gesture_change = current_time
            
            hand_state = self.gesture_cycle[self.current_gesture_idx]
            
            # Draw demo visualization on frame
            self._draw_demo_visualization(frame, hand_state)
            
            return frame, None, hand_state
        
        # If not in demo mode, return no detection
        return frame, None, 'none'
    
    def _draw_demo_visualization(self, frame: Any, hand_state: str) -> None:
        """
        Draw visualization on frame showing current gesture
        """
        h, w = frame.shape[:2]
        
        # Draw semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (w - 10, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Draw title
        cv2.putText(frame, "GESTURE AI DEMO MODE", (20, 40),
                    cv2.FONT_HERSHEY_BOLD, 0.8, (0, 255, 255), 2)
        
        # Draw current gesture
        gesture_text = f"Current Gesture: {hand_state.upper().replace('_', ' ')}"
        cv2.putText(frame, gesture_text, (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw gesture icon/representation
        center_x, center_y = w // 2, h // 2
        
        if hand_state == 'open':
            # Draw open hand (circle with lines)
            cv2.circle(frame, (center_x, center_y), 60, (0, 255, 0), 3)
            for angle in range(0, 360, 72):
                rad = np.radians(angle)
                x = int(center_x + 80 * np.cos(rad))
                y = int(center_y + 80 * np.sin(rad))
                cv2.line(frame, (center_x, center_y), (x, y), (0, 255, 0), 3)
                
        elif hand_state == 'closed':
            # Draw closed fist (filled circle)
            cv2.circle(frame, (center_x, center_y), 50, (0, 0, 255), -1)
            cv2.circle(frame, (center_x, center_y), 50, (255, 255, 255), 3)
            
        elif hand_state == 'swipe_left':
            # Draw left arrow
            cv2.arrowedLine(frame, (center_x + 80, center_y), 
                          (center_x - 80, center_y), (255, 165, 0), 5, tipLength=0.3)
            
        elif hand_state == 'swipe_right':
            # Draw right arrow
            cv2.arrowedLine(frame, (center_x - 80, center_y), 
                          (center_x + 80, center_y), (255, 165, 0), 5, tipLength=0.3)
        
        # Draw progress bar for gesture change
        time_elapsed = time.time() - self.last_gesture_change
        progress = min(time_elapsed / self.gesture_duration, 1.0)
        bar_width = int((w - 40) * progress)
        cv2.rectangle(frame, (20, 100), (20 + bar_width, 110), (0, 255, 255), -1)
        cv2.rectangle(frame, (20, 100), (w - 20, 110), (255, 255, 255), 2)
    
    def get_hand_center(self, landmarks: Optional[Any]) -> Tuple[float, float]:
        """
        Get the center position of the hand
        Returns: (x, y) normalized coordinates
        """
        # In demo mode, return center of frame
        return (0.5, 0.5)
    
    def release(self) -> None:
        """Release resources"""
        pass
