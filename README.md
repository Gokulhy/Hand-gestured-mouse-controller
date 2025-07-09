Hand Gesture Mouse Controller
This Python project allows you to control your mouse cursor and perform clicks using real-time hand gestures detected via your webcam. It provides an intuitive and hands-free way to interact with your computer, ideal for presentations, accessibility, or simply a novel control method.

✨ Features
Cursor Navigation: Move your hand in the webcam's field of view to smoothly navigate the mouse cursor across your screen. The cursor movement is proportional to how far your hand is from a defined central "neutral zone."

Left Click: Perform a left mouse click by holding up three fingers (Index, Middle, Ring).

Right Click: Perform a right mouse click by holding up four fingers (Index, Middle, Ring, Pinky).

Real-time Visualization: The webcam feed displays your hand landmarks and a visual representation of the neutral zone, along with the detected action.

Customizable Sensitivity: Easily adjust cursor speed and click debounce times to suit your preference.

🛠️ Technologies Used
Python 3.x: The core programming language.

OpenCV (cv2): For webcam integration, video stream processing, and drawing visualizations.

MediaPipe Hands (mediapipe): A powerful framework for real-time hand tracking and 21 3D hand landmark detection.

pynput: For simulating mouse movements and clicks at the operating system level.

math module: For mathematical calculations (e.g., distance, if needed for more complex gestures).

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Before running the script, ensure you have Python 3.x installed. Then, install the required libraries using pip:

pip install opencv-python mediapipe pynput

Installation
Clone the repository:

git clone [https://github.com/YourUsername/Hand-Gesture-Mouse-Controller.git](https://github.com/YourUsername/Hand-Gesture-Mouse-Controller.git)
cd Hand-Gesture-Mouse-Controller

(Replace YourUsername with your GitHub username and Hand-Gesture-Mouse-Controller with your actual repository name)

Verify your screen resolution:
Open the gesture-controller.py file and update the SCREEN_WIDTH and SCREEN_HEIGHT variables (around line 34) to match your monitor's actual resolution. This is crucial for accurate cursor mapping.

# Example: For a 1920x1080 monitor
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080 # <-- IMPORTANT: Set your actual screen resolution here!

Running the Script
Execute the Python script from your terminal:

python gesture-controller.py

🎮 Usage
Start the Script: Run the gesture-controller.py file. A window showing your webcam feed will appear.

Position Your Hand: Place your hand clearly in front of your webcam. You'll see landmarks drawn on your hand and a magenta rectangle indicating the "neutral zone."

Navigate Cursor:

Keep your hand's wrist (the base of your palm) within the magenta neutral zone to keep the cursor still.

Move your hand outside this zone to start moving the cursor. The further your hand is from the edge of the neutral zone, the faster the cursor will move.

Left Click: Form a gesture by holding up your Index, Middle, and Ring fingers (3 fingers visible).

Right Click: Form a gesture by holding up your Index, Middle, Ring, and Pinky fingers (4 fingers visible).

Switch Focus: To control other applications, ensure the target application window has focus (click on it with your physical mouse initially).

Quit: Press the 'q' key on your physical keyboard while the webcam window is active to close the application.

⚙️ Customization
You can fine-tune the controller's behavior by adjusting the following global variables in gesture-controller.py:

SCREEN_WIDTH, SCREEN_HEIGHT: (Already mentioned) Crucial for correct cursor mapping.

NEUTRAL_ZONE_X_MIN/MAX, NEUTRAL_ZONE_Y_MIN/MAX: Adjust these (values between 0.0 and 1.0) to change the size and position of the "dead zone" where your hand can rest without moving the cursor.

CURSOR_MOVE_FACTOR_X, CURSOR_MOVE_FACTOR_Y: Control the cursor's speed/sensitivity. Higher values make the cursor move faster.

CLICK_DEBOUNCE_TIME: Sets the minimum time (in seconds) between consecutive clicks of the same type. Increase if you're getting accidental double-clicks, decrease if clicks feel unresponsive.

💡 Potential Improvements & Future Work
Handedness Detection: More robust click detection by explicitly checking if it's a left or right hand.

Dynamic Neutral Zone: A neutral zone that adapts to the user's initial hand position.

Additional Gestures: Implement more gestures for other actions (e.g., scroll, drag-and-drop, keyboard shortcuts).

User Interface: A simple GUI to adjust settings in real-time without editing code.

Multi-Hand Support: Extend to support two hands for more complex interactions.

Calibration Routine: A guided setup for users to calibrate sensitivity and neutral zone.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

📄 License
This project is open-source and available under the MIT License. (You'll need to create a LICENSE file in your repo with the MIT license text)

📧 Contact
Gokul [Your Email/LinkedIn Profile Link]