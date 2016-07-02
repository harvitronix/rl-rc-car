"""
This is a little class that reads from one or more sonar and/or IR sensor.

IR just has a single IN pin that we read from, while sonar has an OUT
and an IN that we interact with.

Example: ir_pins = [24, 25, 28]
Example: sonar_pins = [[24, 25], [28, 29]]
"""
import RPi.GPIO as gpio
import time


class Sensors:
    def __init__(self, ir_pins, sonar_pins):
        self.ir_pins = ir_pins
        self.sonar_pins = sonar_pins

        gpio.setmode(gpio.BCM)

        # Initialize the IR sensors.
        if len(self.ir_pins) > 0:
            for ir in self.ir_pins:
                print("Setting pin %d as IN" % ir)
                gpio.setup(ir, gpio.IN)

        # Initialize the sonar sensors.
        if len(self.sonar_pins) > 0:
            for sonar in self.sonar_pins:
                print("Setting pin %d as OUT, %d as IN" % (sonar[0], sonar[1]))
                gpio.setup(sonar[0], gpio.OUT)
                gpio.setup(sonar[1], gpio.IN)
                gpio.output(sonar[0], False)

        # Wait for sensors to settle.
        print("Initializing sensors.")
        time.sleep(2)
        print("Ready.")

    def get_ir_readings(self):
        readings = []
        for sensor in self.ir_pins:
            readings.append(gpio.input(sensor))
        return readings

    def get_sonar_readings(self):
        readings = []

        for sensor in self.sonar_pins:
            iterations = 0

            # Blip.
            gpio.output(sensor[0], True)
            time.sleep(0.00001)
            gpio.output(sensor[0], False)

            # Read.
            while gpio.input(sensor[1]) == 0 and iterations < 10000:
                pulse_start = time.time()
                iterations += 1

            while gpio.input(sensor[1]) == 1:
                pulse_end = time.time()

            # Turn time into distance.
            try:
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
            except:
                distance = 0

            readings.append(distance)

        return readings

    def cleanup_gpio(self):
        gpio.cleanup()


if __name__ == '__main__':
    # Input pins.
    ir_pins = [24, 21]
    sonar_pins = [[25, 8]]

    sensors = Sensors(ir_pins, sonar_pins)
    for i in range(100):
        print(sensors.get_ir_readings())
        print(sensors.get_sonar_readings())
        time.sleep(2)
    sensors.cleanup_gpio()
