"""
This class controls the RC car itself. It's intended to be the real-world
version of the carmunk simulation.
"""
import RPi.GPIO as GPIO
import time

# Constants
LEFT_PIN = 13
RIGHT_PIN = 15
FORWARD_PIN = 12
BACKWARD_PIN = 11

# Time in seconds to run each action.
# 0 = continuous.
APPLY_TIME = 0.3


class RCCar:
    def __init__(self):
        print("Setting up GPIO pins.")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BACKWARD_PIN, GPIO.OUT)  # Backwards.
        GPIO.setup(FORWARD_PIN, GPIO.OUT)  # Forwards.
        GPIO.setup(LEFT_PIN, GPIO.OUT)  # Left.
        GPIO.setup(RIGHT_PIN, GPIO.OUT)  # Right.

        # Reset in case they're still on from before.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)
        GPIO.output(LEFT_PIN, 0)
        GPIO.output(RIGHT_PIN, 0)

    def cleanup_gpio(self):
        print("Cleaning up GPIO pins.")
        GPIO.cleanup()

    def step(self, action):
        """
        Actions are:
        0: right, forward
        1: left, forward
        2: straight, forward
        3: right, back
        4: left, back
        5: straight, back
        """
        # Forward or back.
        if 0 <= action <= 2:
            # Forwards.
            GPIO.output(BACKWARD_PIN, 0)
            GPIO.output(FORWARD_PIN, 1)
        else:
            # Backwards.
            GPIO.output(FORWARD_PIN, 0)
            GPIO.output(BACKWARD_PIN, 1)

        # Turning.
        if action == 0 or action == 3:  # Turn right.
            GPIO.output(LEFT_PIN, 0)
            GPIO.output(RIGHT_PIN, 1)
            print("Turning right.")
        elif action == 1 or action == 4:  # Turn left.
            GPIO.output(RIGHT_PIN, 0)
            GPIO.output(LEFT_PIN, 1)
            print("Turning left.")
        else:
            GPIO.output(LEFT_PIN, 0)
            GPIO.output(RIGHT_PIN, 0)
            print("Going straight.")

        # Pausing.
        if APPLY_TIME > 0:
            time.sleep(APPLY_TIME)

        # Temporarily stop motion here. Tries to slow things down.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)

    def proximity_alert(self, readings):
        if readings[0] == 0 or readings[2] == 0 or readings[1] < 5:
            return True
        else:
            return False
