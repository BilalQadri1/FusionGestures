from pynput.mouse import Controller as MouseController, Button

class InputController:
    def __init__(self, screen_scale=150, smoothing_factor=0.6):
        self.mouse = MouseController()
        self.screen_scale = screen_scale
        self.smoothing_factor = smoothing_factor  # Exponential smoothing factor

        self.anchor_x = None
        self.anchor_y = None
        self.smooth_curr_x = None
        self.smooth_curr_y = None
        self.current_state = None  # "PAN" (Middle) or "ORBIT" (Right)

    def start_action(self, mode):
        if self.current_state != mode:
            self.stop_action()
            # Tinkercad preset mapping: PAN = Middle Click, ORBIT = Right Click
            btn = Button.middle if mode == "PAN" else Button.right
            self.mouse.press(btn)
            self.current_state = mode

    def stop_action(self):
        if self.current_state is not None:
            btn = Button.middle if self.current_state == "PAN" else Button.right
            self.mouse.release(btn)
            
            self.current_state = None
            self.anchor_x = None
            self.anchor_y = None
            self.smooth_curr_x = None
            self.smooth_curr_y = None

    def handle_gesture(self, gesture, landmark_pos):
        if gesture in ["PAN", "ORBIT"] and landmark_pos is not None:
            raw_x, raw_y = landmark_pos

            if self.current_state != gesture or self.anchor_x is None:
                self.start_action(gesture)
                self.anchor_x = raw_x
                self.anchor_y = raw_y
                self.smooth_curr_x = raw_x
                self.smooth_curr_y = raw_y
                return  

            # Apply EMA smoothing to eliminate webcam micro-jitter
            self.smooth_curr_x = self.smooth_curr_x * self.smoothing_factor + raw_x * (1.0 - self.smoothing_factor)
            self.smooth_curr_y = self.smooth_curr_y * self.smoothing_factor + raw_y * (1.0 - self.smoothing_factor)

            diff_x = self.smooth_curr_x - self.anchor_x
            diff_y = self.smooth_curr_y - self.anchor_y

            dx = int(diff_x * self.screen_scale)
            dy = int(diff_y * self.screen_scale)

            if dx != 0 or dy != 0:
                current_pos = self.mouse.position
                new_x = current_pos[0] + dx
                new_y = current_pos[1] + dy
                self.mouse.position = (new_x, new_y)
        else:
            self.stop_action()

    def release_all(self):
        self.stop_action()