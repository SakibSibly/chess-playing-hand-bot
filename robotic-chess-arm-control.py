import numpy as np
import time
import math
from enum import Enum

class ChessboardDimensions:
    WIDTH = 12  # inches
    HEIGHT = 12  # inches
    SQUARE_SIZE = 1.5  # inches per square

class ArmConfiguration:
    # Arm link lengths (in inches)
    BASE_HEIGHT = 2.0  # Height of base from board
    LINK1_LENGTH = 6.0  # First arm segment
    LINK2_LENGTH = 5.0  # Second arm segment
    GRIPPER_LENGTH = 1.0  # Length of gripper mechanism

    # Motor angle limits (in degrees)
    BASE_ANGLE_MIN = -90
    BASE_ANGLE_MAX = 90
    SHOULDER_ANGLE_MIN = 0
    SHOULDER_ANGLE_MAX = 135
    ELBOW_ANGLE_MIN = -90
    ELBOW_ANGLE_MAX = 90

class ChessboardMapping:
    """
    Maps chess board algebraic notation to physical coordinates
    """
    @staticmethod
    def algebraic_to_coordinates(square):
        """
        Convert chess square (e.g., 'e4') to physical (x,y) coordinates
        
        Args:
            square (str): Chess algebraic notation square
        
        Returns:
            tuple: (x, y) coordinates in inches
        """
        # Chess board is 8x8 squares
        col = ord(square[0].lower()) - ord('a')
        row = int(square[1]) - 1
        
        x = col * ChessboardDimensions.SQUARE_SIZE + (ChessboardDimensions.SQUARE_SIZE / 2)
        y = row * ChessboardDimensions.SQUARE_SIZE + (ChessboardDimensions.SQUARE_SIZE / 2)
        
        return (x, y)

class RoboticChessArmController:
    def __init__(self, motor_controller):
        """
        Initialize Robotic Chess Arm Controller
        
        Args:
            motor_controller: Interface to control physical motors
        """
        self.motor_controller = motor_controller
        self.current_position = None
    
    def inverse_kinematics(self, x, y, z):
        """
        Calculate joint angles for desired end effector position
        
        Args:
            x (float): X coordinate
            y (float): Y coordinate
            z (float): Z coordinate
        
        Returns:
            tuple: Base, shoulder, elbow angles
        """
        # Calculate base rotation (theta1)
        base_angle = math.atan2(y, x) * 180 / math.pi
        
        # Distance from base to target point
        r = math.sqrt(x**2 + y**2)
        
        # Calculate vertical distance
        h = z - ArmConfiguration.BASE_HEIGHT
        
        # Distance from shoulder to end effector
        l = math.sqrt(r**2 + h**2)
        
        # Law of cosines to calculate joint angles
        cos_elbow = (ArmConfiguration.LINK1_LENGTH**2 + ArmConfiguration.LINK2_LENGTH**2 - l**2) / \
                    (2 * ArmConfiguration.LINK1_LENGTH * ArmConfiguration.LINK2_LENGTH)
        
        elbow_angle = math.acos(cos_elbow) * 180 / math.pi
        
        # Shoulder angle calculation
        shoulder_angle = math.atan2(h, r) * 180 / math.pi
        
        return (
            self._constrain_angle(base_angle, ArmConfiguration.BASE_ANGLE_MIN, ArmConfiguration.BASE_ANGLE_MAX),
            self._constrain_angle(shoulder_angle, ArmConfiguration.SHOULDER_ANGLE_MIN, ArmConfiguration.SHOULDER_ANGLE_MAX),
            self._constrain_angle(elbow_angle, ArmConfiguration.ELBOW_ANGLE_MIN, ArmConfiguration.ELBOW_ANGLE_MAX)
        )
    
    def _constrain_angle(self, angle, min_angle, max_angle):
        """
        Constrain angle within specified limits
        
        Args:
            angle (float): Calculated angle
            min_angle (float): Minimum allowed angle
            max_angle (float): Maximum allowed angle
        
        Returns:
            float: Constrained angle
        """
        return max(min_angle, min(max_angle, angle))
    
    def move_piece(self, source_square, destination_square):
        """
        Move a chess piece from source to destination
        
        Args:
            source_square (str): Starting square (e.g., 'e2')
            destination_square (str): Ending square (e.g., 'e4')
        """
        # Convert algebraic notation to coordinates
        source_coords = ChessboardMapping.algebraic_to_coordinates(source_square)
        dest_coords = ChessboardMapping.algebraic_to_coordinates(destination_square)
        
        # Approach heights
        PICK_HEIGHT = 0.5  # inches above board
        MOVE_HEIGHT = 2.0  # inches above board during movement
        
        stages = [
            # 1. Move to source square pickup position
            {'x': source_coords[0], 'y': source_coords[1], 'z': PICK_HEIGHT, 'grip': False},
            # 2. Lower and grip piece
            {'x': source_coords[0], 'y': source_coords[1], 'z': 0, 'grip': True},
            # 3. Lift piece to safe height
            {'x': source_coords[0], 'y': source_coords[1], 'z': MOVE_HEIGHT, 'grip': True},
            # 4. Move to destination square
            {'x': dest_coords[0], 'y': dest_coords[1], 'z': MOVE_HEIGHT, 'grip': True},
            # 5. Lower piece to board
            {'x': dest_coords[0], 'y': dest_coords[1], 'z': 0, 'grip': True},
            # 6. Release piece
            {'x': dest_coords[0], 'y': dest_coords[1], 'z': 0, 'grip': False}
        ]
        
        # Execute movement stages
        for stage in stages:
            # Calculate required joint angles
            base, shoulder, elbow = self.inverse_kinematics(
                stage['x'], stage['y'], stage['z']
            )
            
            # Move motors to calculated positions
            self.motor_controller.move_base(base)
            self.motor_controller.move_shoulder(shoulder)
            self.motor_controller.move_elbow(elbow)
            
            # Control gripper
            if stage['grip']:
                self.motor_controller.close_grip()
            else:
                self.motor_controller.open_grip()
            
            # Short delay for smooth movement
            time.sleep(0.5)
    
    def calibrate(self):
        """
        Calibrate arm to known position
        """
        # Move to home/zero position
        self.motor_controller.move_base(0)
        self.motor_controller.move_shoulder(90)
        self.motor_controller.move_elbow(0)
        self.motor_controller.open_grip()

class MotorController:
    """
    Placeholder for actual motor control interface
    Replace with your specific motor control implementation
    """
    def move_base(self, angle):
        """Rotate base motor to specified angle"""
        print(f"Base motor moved to {angle} degrees")
    
    def move_shoulder(self, angle):
        """Move shoulder motor to specified angle"""
        print(f"Shoulder motor moved to {angle} degrees")
    
    def move_elbow(self, angle):
        """Move elbow motor to specified angle"""
        print(f"Elbow motor moved to {angle} degrees")
    
    def close_grip(self):
        """Close gripper"""
        print("Gripper closed")
    
    def open_grip(self):
        """Open gripper"""
        print("Gripper opened")

# Example usage
def main():
    # Initialize motor controller (replace with your actual implementation)
    motor_ctrl = MotorController()
    
    # Create robotic arm controller
    chess_arm = RoboticChessArmController(motor_ctrl)
    
    # Calibrate arm
    chess_arm.calibrate()
    
    # Move a piece from e2 to e4
    chess_arm.move_piece('e2', 'e4')

if __name__ == "__main__":
    main()
