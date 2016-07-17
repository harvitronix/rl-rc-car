"""
This module holds classes for interacting with our sensors.

Currently supports:
- IR proximity
- Sonar
- IR distance via Arduino

Example: ir_pins = [24, 25, 28]
Example: sonar_pins = [[24, 25], [28, 29]]
"""
import RPi.GPIO as gpio
import time
from statistics import median
import serial
import sys
import json

# Setup the pi.
gpio.setmode(gpio.BCM)


class SonarSensor:
    def __init__(self, in_p, out_p, max_iterations=1000,
                 num_readings=5, max_distance=90):
        self.in_p = in_p
        self.out_p = out_p
        gpio.setup(self.out_p, gpio.OUT)
        gpio.setup(self.in_p, gpio.IN)
        gpio.output(self.out_p, False)
        self.max_distance = max_distance
        self.num_readings = num_readings
        self.max_iterations = max_iterations
        print("Initialized a sonar sensor at %d (in) %d (out)" %
              (self.in_p, self.out_p))

    def get_reading(self):
        """
        Take multiple readings and return the median. Helps with highly
        variant and error-prone readings.
        """
        iterations = 0

        all_readings = []

        for i in range(self.num_readings):
            # Blip.
            gpio.output(self.out_p, True)
            time.sleep(0.00001)
            gpio.output(self.out_p, False)
            pulse_start = None
            pulse_end = None

            # Read.
            while gpio.input(self.in_p) == 0 and iterations < 1000:
                pulse_start = time.time()
                iterations += 1

            iterations = 0  # Reset so we can use it again.
            while gpio.input(self.in_p) == 1 and \
                    iterations < self.max_iterations:
                pulse_end = time.time()
                iterations += 1

            if pulse_start is not None and pulse_end is not None:
                # Turn time into distance.
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150

                # Limit distance returned.
                distance = self.max_distance if \
                    distance > self.max_distance else distance

                # Add the measurement.
                all_readings.append(distance)

        if len(all_readings) > 0:
            return median(all_readings)
        else:
            return self.max_distance


class IRSensor:
    def __init__(self, in_p):
        self.in_p = in_p
        gpio.setup(self.in_p, gpio.IN)
        print("Initialized an IR proximity sensor at %d" %
              (self.in_p))

    def get_reading(self):
        return gpio.input(self.in_p)


class IRDistance:
    """
    Read it from Arduino because it's analog.
    """
    def __init__(self, path='', baud=9600):
        self.ser = serial.Serial(path, baud)
        print("Initialized an IR distance sensor at %s " % path)

    def get_reading(self):
        """Read off the serial port and decode the results."""
        try:
            return self.ser.readline().decode("utf-8").rstrip()
        except:
            return None


class IRSweep:
    """Use a servo to sweep and take readings."""
    def __init__(self, path='', baud=9600):
        self.IRD = IRDistance(path, baud)
        self.readings = [100 for x in range(31)]

    def set_ir_sweep_reading(self):
        """Get IR reading."""
        ir_distance_reading = self.IRD.get_reading()

        # Only update the IR readings if we got a good return value.
        if ir_distance_reading is not None:
            new_sweep = self.update_sweep(ir_distance_reading)
            return new_sweep
        else:
            return None

    def update_sweep(self, reading):
        # Copy the old value.
        new_values = self.readings[:]

        # The reading we get from Arduino is in format "X|Y" where
        # X = the angle and Y = the distance.
        splitup = reading.split('|')
        if isinstance(splitup, list) and len(splitup) == 2 and \
                splitup[0] is not '' and splitup[1] is not '':

            # Get the parts.
            angle = int(splitup[0])
            distance = int(splitup[1])

            # Limit distance returned.
            distance = 90 if distance > 90 else distance

            # Change the angle into an index.
            index = 0 if angle == 0 else int(angle / 6)

            # Update the value at the index.
            try:
                new_values[index] = distance
            except:
                print("Invalid index:")
                print(index)
                raise
        else:
            print('Error reading from IR distance sensor. Received:')
            print(splitup)

        return new_values


class Sensors:
    """
    While the above classes are general to the sensor, this class is used
    specifically to get the sensors we use on Robocar.
    """
    def __init__(self, ir_pins, sonar_pins, arduino_path='/dev/ttyACM0'):
        self.ir_pins = ir_pins
        self.sonar_pins = sonar_pins
        self.arduino_path = arduino_path

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

        # Initialize our IR sensor on the servo.
        try:
            self.ir_sweep = IRSweep(path=self.arduino_path)
        except:
            print("Couldn't find an Arduino at %s" % self.arduino_path)
            print("Exiting.")
            sys.exit(0)

        # Wait for sensors to settle.
        print("Initializing sensors.")
        time.sleep(2)
        print("Ready.")

        # To store readings we'll retrieve from the server.
        self.readings = {
            'ir_l': 1,
            'ir_r': 1,
            's_m': 100,
            'ir_s': self.ir_sweep.readings,
        }

    def set_ir_sweep_reading(self):
        """Get IR reading."""
        new_sweeps = self.ir_sweep.set_ir_sweep_reading()

        if new_sweeps is not None:
            self.readings['ir_s'] = new_sweeps

    def set_ir_proximity_readings(self):
        """Get the proximity readings."""
        ir_reading_l = self.irs[0].get_reading()
        ir_reading_r = self.irs[1].get_reading()

        self.readings['ir_l'] = ir_reading_l
        self.readings['ir_r'] = ir_reading_r

    def set_sonar_reading(self):
        """Get the sonar reading. This happens slowly."""
        sonar_reading = self.sonars[0].get_reading()
        self.readings['s_m'] = int(sonar_reading)

    def cleanup_gpio(self):
        gpio.cleanup()

    def get_all_readings(self):
        return self.readings

    def write_readings(self):
        with open('readings.json', 'w') as f:
            json.dump(self.readings, f)

    def read_readings(self):
        with open('readings.json') as f:
            return json.load(f)
