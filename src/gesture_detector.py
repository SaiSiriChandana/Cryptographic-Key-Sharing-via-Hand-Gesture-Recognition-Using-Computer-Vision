import cv2
from cvzone.HandTrackingModule import HandDetector
import random
import json

# Define gestures and generate randomized binary mapping
GESTURES = ["Thumbs Up", "Peace Sign", "OK Sign"]
BITS_POOL = ['001', '010', '011', '100', '101', '110', '111']
random.shuffle(BITS_POOL)

gesture_to_bits = dict(zip(GESTURES, BITS_POOL[:len(GESTURES)]))

# Save mapping to JSON so it can be reused later (e.g., for decryption)
with open("gesture_map.json", "w") as f:
    json.dump(gesture_to_bits, f)

# Initialize webcam and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
gesture_sequence = []

print("[INFO] Show 3 gestures: Thumbs Up 👍, Peace ✌️, OK 👌")
print(f"[MAPPING] Gesture-to-bit mapping for this session: {gesture_to_bits}")
print("[INFO] After 3 valid gestures, key.txt will be generated.")

while True:
    success, img = cap.read()
    if not success:
        print("[ERROR] Webcam read failed.")
        break

    img = cv2.flip(img, 1)  # Mirror image for user
    hands, img = detector.findHands(img)

    gesture_detected = None

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        
        # Flip hand type for correct mirror display
        handType = "Left" if hand["type"] == "Right" else "Right"

        fingers = detector.fingersUp(hand)

        # Thumbs Up: only thumb up
        if fingers == [1, 0, 0, 0, 0]:
            gesture_detected = "Thumbs Up"

        # Peace Sign: only index and middle fingers up
        elif fingers == [0, 1, 1, 0, 0]:
            gesture_detected = "Peace Sign"

        # OK Sign: thumb and index finger tips close
        elif abs(lmList[4][0] - lmList[8][0]) < 30 and abs(lmList[4][1] - lmList[8][1]) < 30:
            gesture_detected = "OK Sign"

        if gesture_detected and gesture_detected not in gesture_sequence:
            gesture_sequence.append(gesture_detected)
            print(f"[✅] Detected: {gesture_detected} ({handType} hand)")

        # Display gesture name only (not hand type)
        if gesture_detected:
            cv2.putText(img, f"{gesture_detected}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    # Show current gesture sequence
    cv2.putText(img, f"Sequence: {', '.join(gesture_sequence)}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    # If 3 gestures are detected, generate and save key
    if len(gesture_sequence) == 3:
        key_bits = ''.join([gesture_to_bits[g] for g in gesture_sequence])
        with open("key.txt", "w") as f:
            f.write(key_bits)
        print(f"[🔐] Key saved to key.txt: {key_bits}")
        gesture_sequence = []

    cv2.imshow("Gesture Detection", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
