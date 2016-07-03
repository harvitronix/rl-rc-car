"""
This module holds classes for interacting with our sensors.

Currently supports:
- IR proximity
- Sonar

Example: ir_pins = [24, 25, 28]
Example: sonar_pins = [[24, 25], [28, 29]]
"""
import RPi.GPIO as gpio
import time


class SonarSensor:
    def __init__(self, in_p, out_p):
        self.in_p = in_p
        self.out_p = out_p
        gpio.setup(self.out_p, gpio.OUT)
        gpio.setup(self.in_p, gpio.IN)
        gpio.output(self.out_p, False)
        print("Initialized a sonar sensor at %d (in) %d (out)" %
              (self.in_p, self.out_p))

    def get_reading(self):
        iterations = 0

        # Blip.
        gpio.output(self.out_p, True)
        time.sleep(0.00001)
        gpio.output(self.out_p, False)

        # Read.
        while gpio.input(self.in_p) == 0 and iterations < 10000:
            pulse_start = time.time()
            iterations += 1

        while gpio.input(self.in_p) == 1:
            pulse_end = time.time()

        # Turn time into distance.
        try:
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
        except:
            distance = 0

        return distance


class IRSensor:
    def __init__(self, in_p):
        self.in_p = in_p
        gpio.setup(self.in_p, gpio.IN)
        print("Initialized an IR proximity sensor at %d" %
              (self.in_p))

    def get_reading(self):
        return gpio.input(self.in_p)


class Sensors:
    """
    While the above classes are general to the sensor, this class is used
    specifically to get the three sensors we use on Robocar.
    """
    def __init__(self, ir_pins, sonar_pins):
        self.ir_pins = ir_pins
        self.sonar_pins = sonar_pins

        gpio.setmode(gpio.BCM)

        # Initialize the IR sensors.
        self.irs = []
        if len(self.ir_pins) > 0:
            for ir in self.ir_pins:
                self.irs.append(IRSensor(ir))

        # Initialize the sonar sensors.
        self.sonars = []
        if len(self.sonar_pins) > 0:
            for sonar in self.sonar_pins:
                self.sonars.append(SonarSensor(sonar[1], sonar[0]))

        # Wait for sensors to settle.
        print("Initializing sensors.")
        time.sleep(2)
        print("Ready.")

    def get_all_readings(self):
        """
        This is specific to how we need the readings. Should be generalized.
        """
        ir_reading_l = self.irs[0].get_reading()
        ir_reading_r = self.irs[1].get_reading()
        sonar_reading = self.sonars[0].get_reading()

        return [ir_reading_l, int(sonar_reading), ir_reading_r]

    def cleanup_gpio(self):
        gpio.cleanup()


if __name__ == '__main__':
    # Input pins.
    ir_pins = [24, 21]
    sonar_pins = [[25, 8]]

    sensors = Sensors(ir_pins, sonar_pins)
    for i in range(100):
        print(sensors.get_all_readings())
        time.sleep(2)
    sensors.cleanup_gpio()
