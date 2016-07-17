"""
Call the sensors class so we see what they're returning.
"""
from sensors.sensors import Sensors

if __name__ == '__main__':
    # Input pins.
    ir_pins = [24, 21]
    sonar_pins = [[25, 8]]

    sensors = Sensors(ir_pins, sonar_pins)

    while True:
        # Send IR sweep readings on its own path. We do this so that it can
        # read and update at every step, which happens much faster than our
        # silly sonar sensor.
        sensors.set_ir_sweep_reading()
        sensors.set_other_readings()

        # Just to see what's going on.
        print(sensors.get_all_readings())
