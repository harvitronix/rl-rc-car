"""
This class controls the RC car itself. It's intended to be the real-world
version of the carmunk simulation.
"""
import RPi.GPIO as GPIO
import time
import numpy as np
import socket

# Constants
LEFT_PIN = 13
RIGHT_PIN = 15
FORWARD_PIN = 12
BACKWARD_PIN = 11
ITER_PAUSE = 0  # Time to pause between actions for observation.
MOVE_DURATION = 0.3  # Time to apply forward/backward force.
STEERING_DELAY = 0.5  # Time to wait after we move before straightening.

# Used for getting sensor readings.
HOST = '192.168.2.9'
PORT = 8888
SIZE = 1024


class RCCar:
    def __init__(self):
        print("Setting up GPIO pins.")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BACKWARD_PIN, GPIO.OUT)  # Backwards.
        GPIO.setup(FORWARD_PIN, GPIO.OUT)  # Forwards.
        GPIO.setup(LEFT_PIN, GPIO.OUT)  # Left.
        GPIO.setup(RIGHT_PIN, GPIO.OUT)  # Right.

        # Just to make sure.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)
        GPIO.output(LEFT_PIN, 0)
        GPIO.output(RIGHT_PIN, 0)

    def step(self, action):
        self.perform_action(action)

    def cleanup_gpio(self):
        print("Cleaning up GPIO pins.")
        GPIO.cleanup()

    def get_readings(self):
        """
        Call our server on the other Pi to get the readings.
        """
        # Connect to our server to get the reading.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        readings = s.recv(SIZE)
        s.close()

        # Turn our crazy string into an actual list.
        readings = readings.decode('utf-8')
        readings = readings[1:-1]
        readings = readings.split(', ')

        readings = [int(float(i)) for i in readings]

        return np.array([readings])

    def perform_action(self, action):
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
            reverse = False
        else:
            reverse = True

        # Turning.
        if action == 0 or action == 3:  # Turn right.
            GPIO.output(RIGHT_PIN, 1)
            print("Turning right.")
        elif action == 1 or action == 4:  # Turn left.
            GPIO.output(LEFT_PIN, 1)
            print("Turning left.")
        else:
            print("Going straight.")

        # Now that the wheel is turned (or not), move a bit.
        if reverse:
            GPIO.output(BACKWARD_PIN, 1)
        else:
            GPIO.output(FORWARD_PIN, 1)

        # Pause...
        time.sleep(MOVE_DURATION)

        # Now turn off the power.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)

        # Wait a bit longer before turning off the direction.
        # This lets the car wind down in a turn.
        time.sleep(STEERING_DELAY)
        GPIO.output(LEFT_PIN, 0)
        GPIO.output(RIGHT_PIN, 0)

        # Pause just to see what's going on.
        if ITER_PAUSE:
            time.sleep(ITER_PAUSE)

    def proximity_alert(self, readings):
        # If either of the readings show 1, we've detected something.
        if sum(readings) > 0:
            return True
        else:
            return False


if __name__ == '__main__':
    pass
