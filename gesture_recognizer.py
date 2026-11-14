import numpy as np

class GestureRecognizer:
    def __init__(self, pinch_threshold=0.06, debounce_frames=3):
        self.pinch_threshold = pinch_threshold
        self.debounce_frames = debounce_frames
        
        self.pending_gesture = "NEUTRAL"
        self.current_stable_gesture = "NEUTRAL"
        self.streak_count = 0

    def calculate_distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

    def is_pinched(self, lm_list):
        if not lm_list or len(lm_list) < 21:
            return False
        return self.calculate_distance(lm_list[4], lm_list[8]) < self.pinch_threshold

    def recognize(self, all_landmarks):
        raw_gesture = "NEUTRAL"
        target_pos = None

        try:
            if all_landmarks and len(all_landmarks) == 1:
                hand = all_landmarks[0]
                if len(hand) >= 21 and self.is_pinched(hand):
                    raw_gesture = "PAN"
                    target_pos = (hand[8][0], hand[8][1])

            elif all_landmarks and len(all_landmarks) >= 2:
                hand1 = all_landmarks[0]
                hand2 = all_landmarks[1]
                
                if len(hand1) >= 21 and len(hand2) >= 21:
                    if self.is_pinched(hand1) and self.is_pinched(hand2):
                        raw_gesture = "ORBIT"
                        target_pos = (hand2[8][0], hand2[8][1])
                    elif self.is_pinched(hand1):
                        raw_gesture = "PAN"
                        target_pos = (hand1[8][0], hand1[8][1])
        except (IndexError, TypeError):
            # Gracefully catch any frame-drop array anomalies
            raw_gesture = "NEUTRAL"

        # Debounce to filter out single-frame camera or tracking flickers
        if raw_gesture == self.pending_gesture:
            self.streak_count += 1
            if self.streak_count >= self.debounce_frames:
                self.current_stable_gesture = raw_gesture
        else:
            self.pending_gesture = raw_gesture
            self.streak_count = 1

        if self.current_stable_gesture == "PAN" and all_landmarks and len(all_landmarks[0]) >= 21:
            return "PAN", (all_landmarks[0][8][0], all_landmarks[0][8][1])
        elif self.current_stable_gesture == "ORBIT" and all_landmarks and len(all_landmarks) >= 2:
            return "ORBIT", (all_landmarks[1][8][0], all_landmarks[1][8][1])
        
        return "NEUTRAL", None