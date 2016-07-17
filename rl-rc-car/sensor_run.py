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
        # Set all the readings.
        sensors.set_ir_sweep_reading()
        sensors.set_ir_proximity_readings()
        sensors.set_sonar_reading()

        # Write the readings.
        sensors.write_readings()

        # Just to see what's going on.
        print(sensors.get_all_readings())
