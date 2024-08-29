#include <Stepper.h>

const int stepsPerRevolution = 2048;  // Number of steps per revolution (depends on your stepper motor)
const int rolePerMinute = 15;         // Speed of stepper in RPM
const float inchesPerRevolution = 0.025; // Movement per revolution in inches

// Steps to move 0.5mm (500 micrometers)
const int stepsPerMove = 1612;  // Calculated value for 0.5mm move

// Total number of increments to move 1 inch
const int totalIncrements = 51;  // 51 increments to cover approximately 1 inch (25.4mm)

// Initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  // Set the stepper speed
  myStepper.setSpeed(rolePerMinute);

  // Initialize the serial port:
  Serial.begin(9600);

  // Ensure we start from a known position (e.g., at the home or zero position)
  Serial.println("Stepper ready");
}

void loop() {
  for (int i = 0; i < totalIncrements; i++) {
    // Capture a set of 3 images
    Serial.println("CAPTURE");
    waitForCaptureCompletion();

    // Move the actuator 0.5mm forward
    Serial.println("Moving forward 0.5mm");
    myStepper.step(stepsPerMove);
  }

  // Optional: Stop further movement after completing 1 inch
  Serial.println("Completed full inch move");
  while (true) {
    // Stop the loop indefinitely after completing the task
  }
}

void waitForCaptureCompletion() {
  // Wait for the Python script to confirm images have been captured
  while (Serial.available() == 0) {
    // Wait here until data is available
  }
  String response = Serial.readStringUntil('\n');
  if (response == "DONE") {
    delay(500);  // Small delay before the next move, adjust as necessary
  }
}
