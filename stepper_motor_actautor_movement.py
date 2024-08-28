# motor_control.py
# Control a stepper motor using a Raspberry Pi

import time
import RPi.GPIO as GPIO
from stepper import StepperMotor  # Assumes a custom StepperMotor class or use a suitable library

# Constants
STEPS_PER_REVOLUTION = 2048
RPM = 15

# GPIO Pin setup
GPIO.setmode(GPIO.BOARD)  # or GPIO.BCM depending on your pin numbering scheme

# Initialize the stepper motor (assuming pins 8, 10, 9, 11 correspond to GPIO numbers)
stepper_motor = StepperMotor(pins=[8, 10, 9, 11], steps_per_revolution=STEPS_PER_REVOLUTION)

def setup():
    stepper_motor.set_speed(RPM)

def loop():
    # Rotate one revolution clockwise
    print("clockwise")
    stepper_motor.step(STEPS_PER_REVOLUTION)
    time.sleep(0.5)

    # Rotate one revolution counterclockwise
    print("counterclockwise")
    stepper_motor.step(-STEPS_PER_REVOLUTION)
    time.sleep(0.5)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()  # Ensure all GPIO pins are reset
