import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Use the correct port (COMx on Windows)
time.sleep(2)  # Wait for connection

arduino.write(b'1')  # Send data
response = arduino.readline().decode().strip()
print(f"Arduino says: {response}")

arduino.close()
