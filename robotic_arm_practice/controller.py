# import pyfirmata

# comport='/dev/ttyACM0'

# board=pyfirmata.Arduino(comport)


# led_1=board.get_pin('d:8:o')
# led_2=board.get_pin('d:9:o')
# led_3=board.get_pin('d:10:o')
# led_4=board.get_pin('d:11:o')
# led_5=board.get_pin('d:12:o')

# def led(fingerUp):
#     if fingerUp==[0,0,0,0,0]:
#         led_1.write(0)
#         led_2.write(0)
#         led_3.write(0)
#         led_4.write(0)
#         led_5.write(0)

#     elif fingerUp==[0,1,0,0,0]:
#         led_1.write(1)
#         led_2.write(0)
#         led_3.write(0)
#         led_4.write(0)
#         led_5.write(0)
#     elif fingerUp==[0,1,1,0,0]:
#         led_1.write(1)
#         led_2.write(1)
#         led_3.write(0)
#         led_4.write(0)
#         led_5.write(0)    
#     elif fingerUp==[0,1,1,1,0]:
#         led_1.write(1)
#         led_2.write(1)
#         led_3.write(1)
#         led_4.write(0)
#         led_5.write(0)
#     elif fingerUp==[0,1,1,1,1]:
#         led_1.write(1)
#         led_2.write(1)
#         led_3.write(1)
#         led_4.write(1)
#         led_5.write(0)
#     elif fingerUp==[1,1,1,1,1]:
#         led_1.write(1)
#         led_2.write(1)
#         led_3.write(1)
#         led_4.write(1)
#         led_5.write(1)


import pyfirmata2 as pyfirmata
import time

# Check and assign the correct port
comport = '/dev/ttyACM0'

try:
    board = pyfirmata.Arduino(comport)
    print("Connected to Arduino on port:", comport)
except Exception as e:
    print(f"Failed to connect to Arduino on port {comport}. Error: {e}")
    exit(1)

# Initialize LEDs on specific pins
led_pins = [8, 9, 10, 11, 12]
leds = [board.get_pin(f'd:{pin}:o') for pin in led_pins]

def led(fingerUp):
    # Ensure the array is the correct length
    if len(fingerUp) != 5:
        print("Error: fingerUp must be a list of 5 values.")
        return
    
    # Control LEDs based on the fingerUp pattern
    for led, state in zip(leds, fingerUp):
        led.write(state)

try:
    # Example usage
    led([1, 1, 0, 0, 1])
    time.sleep(2)
    led([0, 0, 0, 0, 0])  # Turn off all LEDs
except KeyboardInterrupt:
    print("Process interrupted")
finally:
    # Clean up
    board.exit()
    print("Connection closed")
