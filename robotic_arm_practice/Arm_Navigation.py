import serial
import time

# Set the serial port and baud rate (Make sure this matches your Arduino settings)
arduino = serial.Serial('/dev/ttyACM0', 9600)  # Replace 'COM3' with the correct port
time.sleep(2)  # Wait for the connection to be established

def send_angle_to_arduino(servo, angle):
    """
    Sends the servo and angle to the Arduino.
    """
    arduino.write(f"{servo},{angle}\n".encode())  # Send servo number and angle in the format 'servo,angle'

def move_servo_sequence():
    # Move base servo from 100 to 160 degrees
    for i in range(100, 161, 5):
        send_angle_to_arduino('base', i)
        time.sleep(0.15)

    time.sleep(3)

    # Move shoulder servos from 0 to 30 degrees
    for i in range(0, 31, 5):
        send_angle_to_arduino('shoulder1', i)
        send_angle_to_arduino('shoulder2', 180 - i)
        time.sleep(0.15)

    time.sleep(3)

    # Move farm servo from 100 to 155 degrees
    for i in range(100, 156, 5):
        send_angle_to_arduino('farm', i)
        time.sleep(0.1)

    time.sleep(3)

    # Open grip servo from 0 to 25 degrees
    for i in range(0, 26, 5):
        send_angle_to_arduino('grip', i)
        time.sleep(0.15)

    time.sleep(3)

    # Close grip servo from 25 to 0 degrees
    for i in range(25, -1, -5):
        send_angle_to_arduino('grip', i)
        time.sleep(0.15)

    time.sleep(3)

    # Move farm servo back from 155 to 100 degrees
    for i in range(155, 99, -5):
        send_angle_to_arduino('farm', i)
        time.sleep(0.1)

    time.sleep(3)

    # Move shoulder servos back from 30 to 0 degrees
    for i in range(30, -1, -5):
        send_angle_to_arduino('shoulder1', i)
        send_angle_to_arduino('shoulder2', 180 - i)
        time.sleep(0.15)

    time.sleep(3)

    # Move base servo back from 160 to 100 degrees
    for i in range(160, 99, -5):
        send_angle_to_arduino('base', i)
        time.sleep(0.15)

    time.sleep(3)

# Call the sequence to control the arm
while True:
    move_servo_sequence()

# Close the serial connection after completion
arduino.close()
