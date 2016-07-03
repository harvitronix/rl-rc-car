"""
Drive the car based on a basic algorithm. Used to make sure our sensors
are returning what we expect them to.

Actions are:
0: right, forward
1: left, forward
2: straight, forward
3: right, back
4: left, back
5: straight, back

"""
from rccar import RCCar
from sensor_client import SensorClient

if __name__ == '__main__':
    car = RCCar(apply_time=0.2, wait_time=0.4)
    sensors = SensorClient()

    input("Ready to roll! Press any key to go.")

    for i in range(500):
        # Get readings.
        readings = sensors.get_readings()

        print("Got readings %s" % str(readings))

        # Decide which action to take.
        l_ir = readings[0]
        r_ir = readings[2]
        s = readings[1]

        if s > 10:
            if l_ir == 0:
                action = 0  # Right forward.
            elif r_ir == 0:
                action = 1  # Left forward.
            else:
                action = 2  # Straight forward.
        else:
            if l_ir == 0:
                action = 4  # Left back.
            elif r_ir == 0:
                action = 3  # Right back.
            else:
                action = 4  # Left back.

        print("Taking action %d" % action)

        # Take action.
        car.step(action)

        input("Press enter to take the next step.")
        print("-"*80)
