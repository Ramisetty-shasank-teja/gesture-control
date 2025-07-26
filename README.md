# 🖐️ Gesture-Controlled Human-Computer Interface

A contactless gesture recognition system built with computer vision to enable intuitive control of video playback and virtual mouse interaction using just a standard webcam.    

---

## 📌 Abstract

This project introduces an advanced gesture-controlled system designed to enable seamless human-computer interaction using a standard webcam. Leveraging **MediaPipe** for real-time hand landmark detection and **OpenCV** for live video processing, the system precisely identifies right-hand gestures for intuitive control.

Using **PyAutoGUI** and **PyGetWindow**, the interface offers dual functionality:

- 🎥 **YouTube Control Mode** — Navigate, scroll, select, pause, and browse reels using gestures.
- 🖱️ **Virtual Mouse Mode** — Move the cursor in sync with finger motion; perform left/right clicks using pinch gestures.

The system dynamically switches behavior based on the active window, providing context-aware interactions. It eliminates the need for physical input devices, offering a modern and accessible alternative for touchless control and smart display systems.

---

## 🧠 Features

- 🖐️ Real-time gesture recognition
- 🖱️ Virtual mouse with pinch-based clicks
- 🎞️ Gesture-based YouTube control
- 🪄 Context-aware window detection
- 🧼 Contactless user experience
- 💡 Python-powered with open-source libraries

---

## 💡 Technologies Used

| Module       | Purpose                            |
|--------------|------------------------------------|
| MediaPipe    | Hand landmark detection            |
| OpenCV       | Frame capture and image processing |
| PyAutoGUI    | GUI automation and cursor control  |
| PyGetWindow  | Active window detection            |

---

## 🛠️ Installation & Setup

```bash
git clone https://github.com/your-username/gesture-control-interface.git
cd gesture-control-interface
pip install -r requirements.txt
python main.py
