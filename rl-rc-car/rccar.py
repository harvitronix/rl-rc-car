"""
This class controls the RC car itself. It's intended to be the real-world
version of the carmunk simulation.
"""
import RPi.GPIO as GPIO
import time


class RCCar:
    def __init__(self, left_p=13, right_p=15, forward_p=12, backward_p=11,
                 apply_time=0.3, wait_time=0):
        self.left_p = left_p
        self.right_p = right_p
        self.forward_p = forward_p
        self.backward_p = backward_p
        self.apply_time = apply_time
        self.wait_time = wait_time

        print("Setting up GPIO pins.")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.backward_p, GPIO.OUT)  # Backwards.
        GPIO.setup(self.forward_p, GPIO.OUT)  # Forwards.
        GPIO.setup(self.left_p, GPIO.OUT)  # Left.
        GPIO.setup(self.right_p, GPIO.OUT)  # Right.

        # Reset in case they're still on from before.
        GPIO.output(self.backward_p, 0)
        GPIO.output(self.forward_p, 0)
        GPIO.output(self.left_p, 0)
        GPIO.output(self.right_p, 0)

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
        # Turning.
        if action == 0 or action == 3:  # Turn right.
            GPIO.output(self.left_p, 0)
            GPIO.output(self.right_p, 1)
            print("Turning right.")
        elif action == 1 or action == 4:  # Turn left.
            GPIO.output(self.right_p, 0)
            GPIO.output(self.left_p, 1)
            print("Turning left.")
        else:
            GPIO.output(self.left_p, 0)
            GPIO.output(self.right_p, 0)
            print("Going straight.")

        # Forward or back.
        if 0 <= action <= 2:
            # Forwards.
            GPIO.output(self.backward_p, 0)
            GPIO.output(self.forward_p, 1)
            print("Going forwards.")
        else:
            # Backwards.
            GPIO.output(self.forward_p, 0)
            GPIO.output(self.backward_p, 1)
            print("Going backwards.")

        # Acceling.
        if self.apply_time > 0:
            time.sleep(self.apply_time)

        # Stop moving...
        GPIO.output(self.backward_p, 0)
        GPIO.output(self.forward_p, 0)

        # Wait.
        if self.wait_time > 0:
            time.sleep(self.wait_time)

    def proximity_alert(self, readings):
        if readings['ir_r'] == 0 or readings['ir_l'] == 0:
            return True
        else:
            return False

    def recover(self):
        for i in range(4):
            self.step(4)
