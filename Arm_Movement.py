from math import fabs
import serial
import time

# Set the serial port and baud rate (Make sure this matches your Arduino settings)
arduino = serial.Serial('/dev/ttyACM0', 9600) 
time.sleep(2)


class Arm:
    def __init__(self):

        chessboard = {
            'h8': [180, 25, 155, 170, 20],
            'h7': [170, 25, 155, 165, 25],
            'h6': [160, 30, 150, 152, 25],
            'h5': [150, 35, 145, 144, 25],
            'h4': [150, 38, 142, 130, 25],
            'h3': [145, 45, 135, 115, 20],
            'h2': [],
            'h1': [],
            'g8': [170, 30, 150, 172, 27],
            'g7': [150, 30, 150, 162, 27],
            'g6': [145, 30, 150, 152, 27],
            'g5': [145, 35, 145, 142, 27],
            'g4': [136, 45, 135, 117, 27],
            'g3': [],
            'g2': [],
            'g1': [],
            'f8': [140, 30, 150, 178, 20],
            'f7': [135, 35, 145, 168, 23],
            'f6': [130, 30, 150, 152, 23],
            'f5': [128, 32, 148, 144, 20],
            'f4': [128, 38, 142, 130, 20],
            'f3': [123, 42, 138, 120, 20],
            'f2': [],
            'f1': [],
            'e8': [125, 30, 150, 178, 20],
            'e7': [120, 35, 145, 168, 23],
            'e6': [118, 30, 150, 152, 20],
            'e5': [118, 32, 148, 144, 20],
            'e4': [115, 38, 142, 130, 25],
            'e3': [115, 42, 138, 120, 25],
            'e2': [],
            'e1': [],
            'd8': [],
            'd7': [],
            'd6': [],
            'd5': [],
            'd4': [],
            'd3': [],
            'd2': [],
            'd1': [],
            'c8': [],
            'c7': [],
            'c6': [],
            'c5': [],
            'c4': [],
            'c3': [],
            'c2': [],
            'c1': [],
            'b8': [],
            'b7': [],
            'b6': [],
            'b5': [],
            'b4': [],
            'b3': [],
            'b2': [],
            'b1': [],
            'a8': [],
            'a7': [],
            'a6': [],
            'a5': [],
            'a4': [],
            'a3': [],
            'a2': [],
            'a1': []
        }
        self.initial_position = [100, 0, 180, 100, 0]
        self.current_position = self.initial_position
        self.chessMap         = chessboard
        pass


    def send_angle_to_arduino(self,servo, angle):
        arduino.write(f"{servo},{angle}\n".encode())


    def lift(self):
        base,   shoulder,   shoulder2,   farm,   grip  = self.current_position
        base_i, shoulder_i, shoulder_i2, farm_i, grip_i = self.initial_position

        while grip != grip_i:
            grip += 5     if grip_i > grip else -5
            self.send_angle_to_arduino('grip', grip)
            time.sleep(0.1)

        time.sleep(3)

        while farm != farm_i:
            farm += 5     if farm_i > farm else -5
            self.send_angle_to_arduino('farm', farm)
            time.sleep(0.1)

        time.sleep(3)

        while shoulder != shoulder_i:
            shoulder += 5 if shoulder_i > shoulder else -5
            self.send_angle_to_arduino('shoulder1', shoulder_i)
            self.send_angle_to_arduino('shoulder2', 180 - shoulder)
            time.sleep(0.15)

        time.sleep(3)

        while base != base_i:
            base += 5     if base_i > base else -5
            self.send_angle_to_arduino('base', base)
            time.sleep(0.15)
        
        time.sleep(3)

    def move(self, move_string):
        source      = move_string[:2]
        destination = move_string[2:]

        self.goto(source)
        self.lift()
        self.goto(destination)
        # self.lift()

        # return source, destination
    
    def goto(self,position):
        base_i, shoulder_i, shoulder_i2, farm_i, grip_i = self.initial_position
        base,   shoulder,   shoulder2,   farm,   grip  = self.chessMap[position]


        while base != base_i:
            base_i += 5     if base_i < base else -5
            self.send_angle_to_arduino('base', base_i)
            time.sleep(0.15)
        
        time.sleep(3)

        while shoulder != shoulder_i:
            shoulder_i += 5 if shoulder_i < shoulder else -5
            self.send_angle_to_arduino('shoulder1', shoulder_i)
            self.send_angle_to_arduino('shoulder2', 180 - shoulder_i)
            time.sleep(0.15)

        time.sleep(3)
        
        while farm != farm_i:
            farm_i += 5     if farm_i < farm else -5
            self.send_angle_to_arduino('farm', farm_i)
            time.sleep(0.1)

        time.sleep(3)

        while grip != grip_i:
            grip_i += 5     if grip_i < grip else -5
            self.send_angle_to_arduino('grip', grip_i)
            time.sleep(0.1)

        time.sleep(3)

        self.current_position = (base_i, shoulder_i, 180 - shoulder_i, farm_i, grip_i) 


arm = Arm()
arm.move("a2a4")