"""
Drive without using the trained model. Just a simple algorithm.
"""
from sensor_client import SensorClient
from rccar_client import RCCarClient
from statistics import mean
import time


def get_area_means(ir_sweep):
    area_means = []
    mean_size = 6
    for i in range(0, len(ir_sweep), mean_size):
        area_means.append(mean(ir_sweep[i:i+mean_size]))
    return area_means


def get_max_area(means):
    max_i = 0
    max_mean = 0
    for i, m in enumerate(means):
        if m > max_mean:
            max_mean = m
            max_i = i
    return max_i


def get_proximity(ir_sweep):
    if min(ir_sweep[10:20]) < 22:
        print('Proximity alert!')
        return True
    else:
        return False


def get_action(ir_sweep):
    area_means = get_area_means(ir_sweep)
    print(area_means)
    max_area = get_max_area(area_means)
    print(max_area)

    if max_area == 0 or max_area == 1:
        action = 1  # Turn left.
    elif max_area == 4 or max_area == 5:
        action = 0  # Turn right.
    else:
        action = 2  # Go straight

    return action

if __name__ == '__main__':
    # Setup our two servers.
    sensor_host = '192.168.2.10'
    car_host = '192.168.2.9'

    try:
        sensors = SensorClient(host=sensor_host)
        car = RCCarClient(host=car_host)
    except:
        print("Issue setting up sensors or car.")
        raise

    input("Ready to roll! Press enter to go.")

    while True:
        # Get state.
        readings = sensors.get_readings()
        ir_sweep = readings['state'][:-1]
        print(ir_sweep)

        if get_proximity(ir_sweep):
            car.recover()
            time.sleep(4)
            continue

        # Get action.
        print("Getting action.")
        action = get_action(ir_sweep)
        print("Taking action %d" % action)

        # Take action.
        car.step(action)
        time.sleep(2)

        print("-"*80)

    car.cleanup_gpio()
