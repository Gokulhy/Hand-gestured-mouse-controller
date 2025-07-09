import cv2
import mediapipe as mp
import time
import math # For distance calculations

# Import mouse controller and button types
from pynput.mouse import Controller, Button

# --- Configuration ---
# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, # Focus on a single hand for primary control
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Mouse controller
mouse = Controller()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080 

# Neutral zone (dead zone) around the center of the webcam feed.
NEUTRAL_ZONE_X_MIN = 0.3 # 40% from left
NEUTRAL_ZONE_X_MAX = 0.7 # 60% from left
NEUTRAL_ZONE_Y_MIN = 0.3 # 40% from top
NEUTRAL_ZONE_Y_MAX = 0.7 # 60% from top

# Sensitivity for cursor movement 
CURSOR_MOVE_FACTOR_X = 0.5 # Multiplier for X-axis movement
CURSOR_MOVE_FACTOR_Y = 0.5 # Multiplier for Y-axis movement

# Debounce for clicks to prevent accidental multiple clicks
CLICK_DEBOUNCE_TIME = 0.4 # Minimum time in seconds between clicks

# Last time a click was performed
last_left_click_time = 0
last_right_click_time = 0

# Store the state of the buttons to prevent holding click
is_left_button_down = False
is_right_button_down = False


# --- Hand Pose Recognition for Clicks ---

def is_finger_up(finger_tip_landmark, finger_pip_landmark):
    return finger_tip_landmark.y < finger_pip_landmark.y

def count_fingers_up(hand_landmarks):
    fingers_up = 0

    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x: # For right hand
        pass 

    # Index finger
    if is_finger_up(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]):
        fingers_up += 1
    
    # Middle finger
    if is_finger_up(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]):
        fingers_up += 1

    # Ring finger
    if is_finger_up(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]):
        fingers_up += 1

    # Pinky finger
    if is_finger_up(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]):
        fingers_up += 1
    
    return fingers_up

# --- Main Logic Function ---
def process_hand_gestures(hand_landmarks):
    global last_left_click_time, last_right_click_time, is_left_button_down, is_right_button_down

    current_time = time.time()

    # --- Mouse Cursor Movement ---
    # Use Wrist (Landmark 0) as the reference point for cursor control
    wrist_x_normalized = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
    wrist_y_normalized = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

    # Calculate offset from the center of the neutral zone
    center_x = (NEUTRAL_ZONE_X_MIN + NEUTRAL_ZONE_X_MAX) / 2
    center_y = (NEUTRAL_ZONE_Y_MIN + NEUTRAL_ZONE_Y_MAX) / 2

    offset_x = wrist_x_normalized - center_x
    offset_y = wrist_y_normalized - center_y

    # Determine cursor movement based on hand's position relative to neutral zone
    dx, dy = 0, 0

    # Horizontal movement
    if wrist_x_normalized < NEUTRAL_ZONE_X_MIN:
        dx = (wrist_x_normalized - NEUTRAL_ZONE_X_MIN) * CURSOR_MOVE_FACTOR_X * SCREEN_WIDTH
    elif wrist_x_normalized > NEUTRAL_ZONE_X_MAX:
        dx = (wrist_x_normalized - NEUTRAL_ZONE_X_MAX) * CURSOR_MOVE_FACTOR_X * SCREEN_WIDTH

    # Vertical movement
    if wrist_y_normalized < NEUTRAL_ZONE_Y_MIN:
        dy = (wrist_y_normalized - NEUTRAL_ZONE_Y_MIN) * CURSOR_MOVE_FACTOR_Y * SCREEN_HEIGHT
    elif wrist_y_normalized > NEUTRAL_ZONE_Y_MAX:
        dy = (wrist_y_normalized - NEUTRAL_ZONE_Y_MAX) * CURSOR_MOVE_FACTOR_Y * SCREEN_HEIGHT

    # Move the mouse cursor
    if dx != 0 or dy != 0:
        mouse.move(dx, dy) # move relative to current position
        # print(f"Moving cursor by ({dx:.2f}, {dy:.2f})") # For debugging


    # --- Click Gestures (Static Poses) ---
    fingers_up_count = count_fingers_up(hand_landmarks)
    
    current_action = "Moving Cursor"

    # Left Click: Three fingers up (Index, Middle, Ring)
    if fingers_up_count == 3:
        if current_time - last_left_click_time > CLICK_DEBOUNCE_TIME:
            mouse.click(Button.left)
            last_left_click_time = current_time
            current_action = "Left Click"
            print("Left Click!")
            is_left_button_down = True
        # else:
        #    print("Left Click (debounced)")
    elif is_left_button_down: # Release the button if 3 fingers no longer detected
        mouse.release(Button.left)
        is_left_button_down = False

    # Right Click: Four fingers up (Index, Middle, Ring, Pinky)
    elif fingers_up_count == 4:
        if current_time - last_right_click_time > CLICK_DEBOUNCE_TIME:
            mouse.click(Button.right)
            last_right_click_time = current_time
            current_action = "Right Click"
            print("Right Click!")
            is_right_button_down = True
        # else:
        #    print("Right Click (debounced)")
    elif is_right_button_down: # Release the button if 4 fingers no longer detected
        mouse.release(Button.right)
        is_right_button_down = False
    
    # If no specific click gesture, ensure buttons are released
    if fingers_up_count != 3 and is_left_button_down:
        mouse.release(Button.left)
        is_left_button_down = False
    if fingers_up_count != 4 and is_right_button_down:
        mouse.release(Button.right)
        is_right_button_down = False

    return current_action

# --- Main Loop ---
def main():
    cap = cv2.VideoCapture(0) # 0 for default webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("--- Hand Gesture Mouse Controller ---")
    print(f"Screen Resolution Set To: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"Neutral Zone (normalized): X: {NEUTRAL_ZONE_X_MIN}-{NEUTRAL_ZONE_X_MAX}, Y: {NEUTRAL_ZONE_Y_MIN}-{NEUTRAL_ZONE_Y_MAX}")
    print(f"Cursor Sensitivity (X): {CURSOR_MOVE_FACTOR_X} units")
    print(f"Cursor Sensitivity (Y): {CURSOR_MOVE_FACTOR_Y} units")
    print("Controls:")
    print("  Move Hand: Navigate Cursor (proportional to distance from center)")
    print("  3 Fingers Up (no thumb): Left Click")
    print("  4 Fingers Up (no thumb): Right Click")
    print("Press 'q' to quit.")
    print("-----------------------------")

    mouse.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        detected_display_text = "Waiting for Hand..."

        # Draw neutral zone on the frame for visualization
        h, w, _ = frame.shape
        cv2.rectangle(frame, 
                      (int(NEUTRAL_ZONE_X_MIN * w), int(NEUTRAL_ZONE_Y_MIN * h)),
                      (int(NEUTRAL_ZONE_X_MAX * w), int(NEUTRAL_ZONE_Y_MAX * h)),
                      (255, 0, 255), 2) # Magenta rectangle

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Process gestures and control mouse
                detected_display_text = process_hand_gestures(hand_landmarks)

        else:
            # If no hand is detected, reset click states
            global is_left_button_down, is_right_button_down
            if is_left_button_down:
                mouse.release(Button.left)
                is_left_button_down = False
            if is_right_button_down:
                mouse.release(Button.right)
                is_right_button_down = False
            

        # Display the detected gesture/action on the frame
        cv2.putText(frame, f"Action: {detected_display_text}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.imshow('Hand Gesture Mouse Controller', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()