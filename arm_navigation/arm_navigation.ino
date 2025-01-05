#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Create the PCA9685 object
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Define servo channels
#define shoulder1 0
#define shoulder2 1
#define farm 2
#define grip 3
#define base 4


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

  pwm.setPWM(shoulder1, 0, angleToPulse(0));
//  delay(1000);
  pwm.setPWM(shoulder2, 0, angleToPulse(180));
//    delay(3000);
  pwm.setPWM(farm, 0, angleToPulse(0));
//    delay(1000);
  pwm.setPWM(grip, 0, angleToPulse(0));
  pwm.setPWM(base, 0, angleToPulse(120));


}

void loop() {
  
  for (int i = 0; i <= 180; i += 5) {
    pwm.setPWM(shoulder1, 0, angleToPulse(i));
    pwm.setPWM(shoulder2, 0, angleToPulse(180 - i));

    delay(150);
  }

  delay(5000);

  for(int i=0; i<=90; i+=5){
  pwm.setPWM(farm, 0, angleToPulse(i));
  delay(100);
  }

delay(5000);
  
  for (int i = 180; i >= 0; i -= 5) {
    pwm.setPWM(shoulder1, 0, angleToPulse(i));
    pwm.setPWM(shoulder2, 0, angleToPulse(180 - i));

    delay(150);
    
  }
  
  delay(5000);

  for (int i = 0; i <= 90; ++i) {
    pwm.setPWM(grip, i, angleToPulse(i));
    delay(100);
  }

  delay(2000);

  for (int i = 90; i >= 0; --i) {
    pwm.setPWM(grip, i, angleToPulse(i));
    delay(100);
  }
  delay(2000);

  for(int i=90; i>=0; i-=5){
  pwm.setPWM(farm, 0, angleToPulse(i));
  delay(100);
}

delay(5000);

}
