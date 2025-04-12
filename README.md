# Virtual_Keyboard_AiProject
# Virtual Keyboard with Hand Gestures 🖐️⌨️

[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)

A **touchless virtual keyboard** that uses hand tracking to detect gestures and simulate key presses. Control your computer using just your fingers and a webcam!

![Demo](demo.gif)  
*(Replace with actual demo GIF/screenshot)*

---

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)


---

## Features ✨
- Real-time hand tracking using **MediaPipe**
- QWERTY keyboard layout visualization
- Key press detection via **index and middle finger proximity**
- Visual feedback for button hovers and clicks
- Terminal display of typed text
- Exit with a single 'q' key press

---

## Technologies Used 💻
| Technology       | Purpose                          |
|------------------|----------------------------------|
| **OpenCV**       | Webcam input and image processing |
| **MediaPipe**    | Hand landmark detection          |
| **PyAutoGUI**    | Simulating keyboard presses      |
| **NumPy**        | Distance calculations            |

---

## Installation 🛠️

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/virtual-keyboard.git
   cd virtual-keyboard
2.**Install dependencies**
```bash
pip install opencv-python mediapipe pyautogui numpy



