# FusionGesture

A lightweight, background macOS menu bar utility that transforms your standard webcam into a gesture-controlled 3D mouse for **Autodesk Fusion 360**. 

Designed to eliminate ergonomic friction and bridge the gap between computer vision and CAD software, `FusionGesture` lets you seamlessly pan, orbit, and navigate 3D models using natural hand gestures.

---

## Key Features

- **Native macOS Menu Bar Integration**: Runs quietly as a background accessory (`LSUIElement`) with zero Dock clutter, featuring a custom menu bar toggle and clean hardware control.
- **Hardware Privacy Lifecycle**: Dynamically manages camera streams (`cv2.VideoCapture`). Toggling the app to "Off" completely releases the camera hardware handle, immediately extinguishing the MacBook's physical green LED indicator.
- **Dual-Hand 3D Navigation**:
  - **1 Hand Pinched**: Pan (Middle Mouse Drag)
  - **2 Hands Pinched**: Orbit / Rotate (Right Mouse Drag)
- **Jitter-Free Control**: Implements exponential moving average (EMA) smoothing and frame-deboucing logic to ensure buttery-smooth cursor tracking without jitter.
- **Standalone Distribution**: Fully bundleable into a native macOS `.app` package via PyInstaller for easy deployment and login item automation.

---

## Tech Stack & Architecture

- **Language**: Python 3.10+
- **Computer Vision & Tracking**: OpenCV, Google MediaPipe (Hand Landmarker model)
- **UI & System Integration**: `rumps` (Gorgeous Menu Bar Python wrapper), PyObjC (Cocoa API bindings for thread safety and window management)
- **Input Simulation**: `pynput` for cross-platform mouse event emulation
- **Concurrency**: Multi-threaded architecture separating the main Cocoa event loop (UI) from the background computer vision inference loop.
