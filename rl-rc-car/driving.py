"""
This is the real-world equivalent of the simulation's learning.py.
"""
from becho import becho, bechonet
from rccar import RCCar
from sensor_client import SensorClient
import numpy as np

if __name__ == '__main__':
    network = bechonet.BechoNet(
        num_actions=6, num_inputs=3,
        nodes_1=256, nodes_2=256, verbose=True,
        load_weights=True,
        weights_file='saved-models/sonar-and-ir-3750.h5'
    )
    pb = becho.ProjectBecho(
        network, num_actions=6, num_inputs=3,
        verbose=True, enable_training=False
    )
    car = RCCar(apply_time=0.2, wait_time=0.5)
    sensors = SensorClient()

    input("Ready to roll! Press any key to go.")

    for i in range(500):
        readings = sensors.get_readings()
        readings = np.array([readings])
        action = pb.get_action(readings)
        car.step(action)

        print(readings)

        if car.proximity_alert(readings):
            print('Proximity alert!')

        print("-"*80)

    car.cleanup_gpio()
