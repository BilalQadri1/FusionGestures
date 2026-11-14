import argparse
import sys
import time
import threading
import cv2
import AppKit

from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from input_controller import InputController
from menubar_app import FusionMenuApp

def vision_processing_loop(menu_app, args):
    """Runs the OpenCV and MediaPipe tracking loop with full hardware camera lifecycle management."""
    tracker = HandTracker(max_hands=2)
    recognizer = GestureRecognizer(pinch_threshold=0.06, debounce_frames=3)
    controller = InputController(screen_scale=150, smoothing_factor=0.6)

    cap = None

    try:
        while menu_app.is_running:
            # If toggled off, release the camera hardware so the green light turns off
            if not menu_app.is_active:
                if cap is not None:
                    controller.release_all()
                    cap.release()
                    cap = None
                    print(">> Camera released (Green light off).")
                time.sleep(0.2)
                continue

            # If toggled on and camera isn't active, initialize it fresh
            if cap is None:
                print(">> Opening camera...")
                cap = cv2.VideoCapture(args.camera)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 30)
                
                # Brief pause to let macOS hardware bind the stream cleanly
                time.sleep(0.5)

                if not cap.isOpened():
                    print("Error: Could not open webcam. Retrying...")
                    cap = None
                    time.sleep(1.0)
                    continue
                print(">> Webcam active. Tracking started...")

            success, frame = cap.read()
            if not success:
                time.sleep(0.05)
                continue

            frame = cv2.flip(frame, 1)
            frame, all_landmarks = tracker.find_hands(frame, draw=False)

            gesture, landmark_pos = recognizer.recognize(all_landmarks)
            
            controller.handle_gesture(gesture, landmark_pos)
            menu_app.update_mode(gesture)

            time.sleep(0.01)

    except Exception as e:
        print(f"Vision loop error: {e}")
    finally:
        controller.release_all()
        if cap is not None:
            cap.release()
        tracker.release()

def main():
    parser = argparse.ArgumentParser(description="Fusion 360 Controller with Menu Bar Support")
    parser.add_argument("--camera", type=int, default=0, help="Webcam device index")
    args = parser.parse_args()

    # Hide the Python rocket ship icon from the macOS Dock/Taskbar
    app = AppKit.NSApplication.sharedApplication()
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)

    print("=" * 60)
    print(" Fusion 360 Controller Initialized (Background Menu Bar Mode)...")
    print(" Controls:")
    print("   - 1 Hand Pinched: PAN (Middle Mouse Drag)")
    print("   - 2 Hands Pinched: ORBIT / ROTATE (Right Mouse Drag)")
    print("   - Menu Bar (Top Right): Click icon to toggle On/Off")
    print("=" * 60)

    # Initialize Menu Bar App on the main thread
    menu_app = FusionMenuApp()

    # Spin up the OpenCV tracking loop on a background thread
    vision_thread = threading.Thread(target=vision_processing_loop, args=(menu_app, args), daemon=True)
    vision_thread.start()

    # Start rumps on the MAIN thread (required by macOS Cocoa)
    menu_app.run()

if __name__ == "__main__":
    main()