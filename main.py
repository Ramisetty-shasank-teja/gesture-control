import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time

# Screen resolution
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_click = False
prev_right_click = False

def get_active_platform():
    window_title = gw.getActiveWindowTitle() or ""
    if "YouTube" in window_title:
        return "youtube"
    return "other"

def get_finger_status(landmarks):
    finger_status = []
    tips = [mp_hands.HandLandmark.THUMB_TIP,
            mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.PINKY_TIP]

    pips = [mp_hands.HandLandmark.THUMB_IP,
            mp_hands.HandLandmark.INDEX_FINGER_PIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
            mp_hands.HandLandmark.RING_FINGER_PIP,
            mp_hands.HandLandmark.PINKY_PIP]

    for tip, pip in zip(tips, pips):
        finger_status.append(landmarks.landmark[tip].y < landmarks.landmark[pip].y)

    return finger_status  # [thumb, index, middle, ring, pinky]

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    platform = get_active_platform()

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        finger_open = get_finger_status(hand_landmarks)
        thumb, index, middle, ring, pinky = finger_open

        # Coordinates
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)
        screen_x = int(index_tip.x * screen_width)
        screen_y = int(index_tip.y * screen_height)

        # Move mouse cursor
        pyautogui.moveTo(screen_x, screen_y)

        # YouTube specific gestures
        if platform == "youtube":
            if index and not any([middle, ring, pinky, thumb]):
                print("➡ Next Reel")
                pyautogui.press('down')

            elif index and middle and not any([ring, pinky, thumb]):
                print("⬅ Previous Reel")
                pyautogui.press('up')

            elif all(finger_open):
                print("▶ Resume")
                pyautogui.press('space')

            elif not any(finger_open):
                print("⏸ Pause")
                pyautogui.press('space')

            elif thumb and not any([index, middle, ring, pinky]) and thumb_tip.x < 0.3:
                print("⬅ Back Page")
                pyautogui.hotkey('alt', 'left')

            elif pinky and not any([index, middle, ring, thumb]) and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x + 0.1:
                print("➡ Forward Page")
                pyautogui.hotkey('alt', 'right')

            elif index and not any([middle, ring, pinky, thumb]) and index_y < height * 0.4:
                print("⬆ Scroll Up")
                pyautogui.scroll(30)

            elif index and thumb and abs(index_x - int(thumb_tip.x * width)) > 100:
                print("⬇ Scroll Down")
                pyautogui.scroll(-30)

            elif index and thumb and abs(index_x - int(thumb_tip.x * width)) < 40 and abs(index_y - int(thumb_tip.y * height)) < 40:
                print("🔘 Select / Pause")
                pyautogui.click()

        # Universal Virtual Mouse Clicks
        # Left click (Index + Thumb pinch)
        if index and thumb:
            dist = abs(index_x - int(thumb_tip.x * width)) + abs(index_y - int(thumb_tip.y * height))
            if dist < 40 and not prev_click:
                print("🖱 Left Click")
                pyautogui.click()
                prev_click = True
            elif dist >= 40:
                prev_click = False

        # Right click (Index + Middle pinch)
        if index and middle:
            dist = abs(index_x - int(middle_tip.x * width)) + abs(index_y - int(middle_tip.y * height))
            if dist < 40 and not prev_right_click:
                print("🖱 Right Click")
                pyautogui.click(button='right')
                prev_right_click = True
            elif dist >= 40:
                prev_right_click = False

    cv2.imshow("Gesture Control System (YouTube + Virtual Mouse)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()