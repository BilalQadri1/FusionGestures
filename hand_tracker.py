import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=2, detection_con=0.7, tracking_con=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=tracking_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=False):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        all_landmarks = []

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    lm_list.append((lm.x, lm.y, lm.z))
                all_landmarks.append(lm_list)
                
        return frame, all_landmarks

    def release(self):
        self.hands.close()