import cv2
import controller as cnt
from cvzone.HandTrackingModule import HandDetector
import pyfirmata2 as pyfirmata
import time

# Define comport
comport = '/dev/ttyACM0'

# Function to connect to Arduino and initialize pins
def connect_arduino(comport):
    try:
        board = pyfirmata.Arduino(comport)
        print("Connected to Arduino on port:", comport)
        
        # Start an iterator to keep the connection alive
        it = pyfirmata.util.Iterator(board)
        it.start()
        return board
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

# Initialize Arduino board and LEDs
board = connect_arduino(comport)
led_pins = [8, 9, 10, 11, 12]
leds = [board.get_pin(f'd:{pin}:o') for pin in led_pins] if board else []

def led(fingerUp):
    if len(fingerUp) != 5:
        print("Error: fingerUp must be a list of 5 values.")
        return
    
    # Try to write to LEDs, handle port errors
    for led, state in zip(leds, fingerUp):
        try:
            led.write(state)
        except pyfirmata.serial.SerialException:
            print("Lost connection. Reconnecting...")
            reconnect()

def reconnect():
    global board, leds
    board = connect_arduino(comport)
    if board:
        leds = [board.get_pin(f'd:{pin}:o') for pin in led_pins]
    else:
        print("Reconnection failed")

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = cv2.flip(frame, 1)
    hands, img = detector.findHands(frame)

    if hands:
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)
        print(fingerUp)
        
        # Control LEDs and display finger count
        led(fingerUp)
        finger_count = fingerUp.count(1)
        cv2.putText(frame, f'Finger count: {finger_count}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("frame", frame)
    
    # Exit loop when 'k' is pressed
    if cv2.waitKey(1) == ord("k"):
        break

video.release()
cv2.destroyAllWindows()

if board:
    board.exit()
    print("Connection closed")