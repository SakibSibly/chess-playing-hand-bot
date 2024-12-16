#include <Servo.h>
#include <math.h>

// Arm Dimensions (in cm)
const float L1 = 10.0; // Shoulder link length
const float L2 = 15.0; // Elbow link length

// Servo Objects
Servo baseServo, shoulderServo, elbowServo, gripperServo;

// Function to Calculate and Move Arm to Target
void moveTo(float x, float y, float z) {
  // Base Angle (Theta 0)
  float theta0 = atan2(y, x) * 180 / M_PI; // Convert to degrees

  // Distance to Target
  float d = sqrt(x * x + y * y);

  // Check if Target is Reachable
  if (d > (L1 + L2)) {
    Serial.println("Target out of reach!");
    return;
  }

  // Elbow Angle (Theta 2)
  float cosTheta2 = (L1 * L1 + L2 * L2 - d * d) / (2 * L1 * L2);
  float theta2 = acos(cosTheta2) * 180 / M_PI; // Convert to degrees

  // Shoulder Angle (Theta 1)
  float phi = atan2(z, d); // Vertical angle
  float psi = acos((d * d + L1 * L1 - L2 * L2) / (2 * d * L1));
  float theta1 = (phi - psi) * 180 / M_PI; // Convert to degrees

  // Gripper Orientation (Theta 3)
  float theta3 = 90.0; // Keep gripper horizontal

  // Move Servos
  baseServo.write(theta0);
  delay(500);
  shoulderServo.write(theta1);
  delay(500);
  elbowServo.write(theta2);
  delay(500);
  gripperServo.write(theta3);
  delay(500);

  // Print Angles
  Serial.print("Theta 0: "); Serial.println(theta0);
  Serial.print("Theta 1: "); Serial.println(theta1);
  Serial.print("Theta 2: "); Serial.println(theta2);
  Serial.print("Theta 3: "); Serial.println(theta3);
}

void setup() {
  Serial.begin(9600);

  // Attach Servos
  baseServo.attach(9);
  shoulderServo.attach(10);
  elbowServo.attach(11);
  gripperServo.attach(12);

  // Initialize Servos
  baseServo.write(90);
  shoulderServo.write(90);
  elbowServo.write(90);
  gripperServo.write(90);
}

void loop() {
  // Example: Move to (15, 15, 5)
  moveTo(15, 15, 5);

  // Delay before next move
  delay(5000);
}
