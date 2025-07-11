# Hand Gesture Mouse Controller

A computer vision-based mouse controller that uses hand gestures to control your computer's cursor and clicking functionality. This project leverages MediaPipe for hand tracking and OpenCV for video processing to provide touchless mouse control.

## Features

- **Cursor Movement**: Control mouse cursor by moving your hand within the camera's view
- **Left Click**: Raise 3 fingers (index, middle, ring) to perform left clicks
- **Right Click**: Raise 4 fingers (index, middle, ring, pinky) to perform right clicks
- **Neutral Zone**: Dead zone in the center of the screen to prevent accidental movements
- **Click Debouncing**: Prevents accidental multiple clicks with configurable delay
- **Visual Feedback**: Real-time display of hand landmarks and current action

## Requirements

### Dependencies

```bash
pip install opencv-python mediapipe pynput
```

### System Requirements

- Python 3.7+
- Webcam/Camera
- Windows/macOS/Linux (Note: Some systems may require additional permissions for mouse control)

## Usage

1. **Start the Application**: Run `python gesture-controller.py`
2. **Position Your Hand**: Place your hand in front of the camera
3. **Cursor Control**: Move your hand to control the cursor (outside the neutral zone)
4. **Left Click**: Raise 3 fingers (index, middle, ring) - excluding thumb
5. **Right Click**: Raise 4 fingers (index, middle, ring, pinky) - excluding thumb
6. **Exit**: Press 'q' to quit the application

### Controls Summary

| Gesture | Action |
|---------|--------|
| Hand Movement | Cursor movement (proportional to distance from center) |
| 3 Fingers Up | Left Click |
| 4 Fingers Up | Right Click |
| 'q' Key | Quit application |

## Configuration

The application includes several configurable parameters in the script:

### Screen Resolution
```python
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
```

### Neutral Zone (Dead Zone)
```python
NEUTRAL_ZONE_X_MIN = 0.3  # 30% from left
NEUTRAL_ZONE_X_MAX = 0.7  # 70% from left
NEUTRAL_ZONE_Y_MIN = 0.3  # 30% from top
NEUTRAL_ZONE_Y_MAX = 0.7  # 70% from top
```

### Cursor Sensitivity
```python
CURSOR_MOVE_FACTOR_X = 0.5  # X-axis movement multiplier
CURSOR_MOVE_FACTOR_Y = 0.5  # Y-axis movement multiplier
```

### Click Debouncing
```python
CLICK_DEBOUNCE_TIME = 0.4  # Minimum time between clicks (seconds)
```

### MediaPipe Settings
```python
min_detection_confidence=0.7  # Hand detection confidence threshold
min_tracking_confidence=0.5   # Hand tracking confidence threshold
```

## Technical Details

### Hand Tracking
- Uses MediaPipe Hands for real-time hand landmark detection
- Tracks 21 hand landmarks per detected hand
- Focuses on single-hand detection for primary control

### Gesture Recognition
- Finger counting based on landmark positions
- Thumb detection currently optimized for right hand
- Wrist position used as reference point for cursor movement

### Mouse Control
- Utilizes pynput library for cross-platform mouse control
- Relative movement based on hand position offset from neutral zone
- Debounced clicking to prevent multiple rapid clicks


## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand tracking capabilities
- [OpenCV](https://opencv.org/) for computer vision processing
- [pynput](https://pypi.org/project/pynput/) for mouse control functionality
