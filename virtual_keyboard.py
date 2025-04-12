import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
]

# Button dimensions and spacing
BUTTON_WIDTH = 60
BUTTON_HEIGHT = 60
HORIZONTAL_SPACING = 70  # Space between keys
VERTICAL_SPACING = 80    # Space between rows
START_X = 50             # Left margin
START_Y = 100            # Top margin

class Button:
    def __init__(self, pos, text, size=[BUTTON_WIDTH, BUTTON_HEIGHT]):
        self.pos = pos
        self.size = size
        self.text = text

# Initialize camera with larger resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Hand detector setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Create buttons with adjusted positions
buttonList = []
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        x = START_X + (HORIZONTAL_SPACING * j)
        y = START_Y + (VERTICAL_SPACING * i)
        buttonList.append(Button([x, y], key))

def drawAll(img, buttons):
    for button in buttons:
        x, y = button.pos
        w, h = button.size
        # Draw button
        cv2.rectangle(img, (x, y), (x + w, y + h), (175, 0, 175), cv2.FILLED)
        # Draw text
        cv2.putText(img, button.text, (x + 15, y + 45),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    return img
#start of main loop

final_text = ""
last_press_time = 0
exit_program = False

while not exit_program:
    success, img = cap.read()
    if not success:
        continue

     # Check for exit key FIRST
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        print("\nExiting virtual keyboard...")
        exit_program = True
        break  # Immediate exit


    # # Flip and resize image
    # img = cv2.flip(img, 1)
    # img = cv2.resize(img, (1280, 720))
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     # Flip and resize image
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (1280, 720))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process hands
    results = hands.process(img_rgb)
    img = drawAll(img, buttonList)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get finger landmarks
            h, w, _ = img.shape
            x8 = int(hand_landmarks.landmark[8].x * w)  # Index finger
            y8 = int(hand_landmarks.landmark[8].y * h)
            x12 = int(hand_landmarks.landmark[12].x * w)  # Middle finger
            y12 = int(hand_landmarks.landmark[12].y * h)

            # Check button hover
            for button in buttonList:
                x, y = button.pos
                w_btn, h_btn = button.size

                # Hover effect
                if x < x8 < x + w_btn and y < y8 < y + h_btn:
                    cv2.rectangle(img, (x-5, y-5), 
                                  (x + w_btn + 5, y + h_btn + 5),
                                  (0, 255, 0), 2)

                    # Calculate finger distance
                    distance = np.hypot(x8 - x12, y8 - y12)

                    # Click detection
                    if distance < 30 and (time.time() - last_press_time) > 0.3:
                        pyautogui.press(button.text)
                        final_text += button.text
                        print(f"Pressed: {button.text}")
                        print(f"Current Text: {final_text}")
                        last_press_time = time.time()

                        # Visual feedback
                        cv2.rectangle(img, (x, y), 
                                      (x + w_btn, y + h_btn),
                                      (0, 255, 0), cv2.FILLED)

    # Display typed text
    cv2.putText(img, final_text[-20:], (50, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # Show output
    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()