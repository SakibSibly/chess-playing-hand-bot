#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Create the PCA9685 object
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Define servo channels
#define base 0
#define shoulder1 1
#define shoulder2 2
#define farm 3
#define grip 4



// Define the pulse length range for the servos
#define SERVOMIN 150  // Minimum pulse length count
#define SERVOMAX 600  // Maximum pulse length count

// Function to convert angle (0-180) to PWM pulse length
int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Initializing PCA9685...");
  
  pwm.begin();
  pwm.setPWMFreq(90); // Analog servos run at 50 Hz
  delay(10);
  
  pwm.setPWM(base, 0, angleToPulse(100));
  int ii = 0;
  pwm.setPWM(shoulder1, 0, angleToPulse(ii));

  pwm.setPWM(shoulder2, 0, angleToPulse(180-ii));

  pwm.setPWM(farm, 0, angleToPulse(100));

  pwm.setPWM(grip, 0, angleToPulse(0));



}

void loop() { 

  for (int i = 100; i <= 160; i += 5) {
    pwm.setPWM(base, 0, angleToPulse(i));
    delay(150);
  }
  delay(3000);
  
  for (int i = 0; i <= 30; i += 5) {
    pwm.setPWM(shoulder1, 0, angleToPulse(i));
    pwm.setPWM(shoulder2, 0, angleToPulse(180 - i));

    delay(150);
  }

  delay(3000);

  for(int i = 100; i <= 155; i += 5) {
    pwm.setPWM(farm, 0, angleToPulse(i));
    delay(100);
  }

  delay(3000);

  for (int i = 0; i <= 25; i += 5) {
    pwm.setPWM(grip, 0, angleToPulse(i));
    delay(150);
  }
  
  delay(3000);

    for (int i = 25; i >= 0; i -= 5) {
    pwm.setPWM(grip, 0, angleToPulse(i));
    delay(150);
  }
  
  delay(3000);

    for(int i = 155; i >= 100; i -= 5) {
    pwm.setPWM(farm, 0, angleToPulse(i));
    delay(100);
  }

  delay(3000);

  for (int i = 30; i >= 0; i -= 5) {
    pwm.setPWM(shoulder1, 0, angleToPulse(i));
    pwm.setPWM(shoulder2, 0, angleToPulse(180 - i));

    delay(150);
  }

  delay(3000);

  for (int i = 160; i >= 100; i -= 5) {
    pwm.setPWM(base, 0, angleToPulse(i));
    delay(150);
  }
  delay(3000);
  

}
