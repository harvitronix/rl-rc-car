"""
This file holds a class that deals with reading from our two IR
sensors. It's called from a server, so it doesn't need to deal with
looping/reading many times. Rather, it will be called, get the readings,
and then return them.
"""
import RPi.GPIO as GPIO
import time

# Input pins.
# PINS = [24, 21]
PINS = [21]


class Sensors:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Initialize the sensors.
        for sensor in PINS:
            GPIO.setup(sensor, GPIO.IN)

    def get_readings(self):
        readings = []
        for sensor in PINS:
            readings.append(GPIO.input(sensor))

        return readings

    def cleanup_gpio(self):
        GPIO.cleanup()


if __name__ == '__main__':
    sensors = Sensors()
    for i in range(100):
        print(sensors.get_readings())
        time.sleep(2)
    sensors.cleanup_gpio()
