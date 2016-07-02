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
        weights_file='saved-models/sonar-and-ir-9750.h5'
    )
    pb = becho.ProjectBecho(
        network, num_actions=6, num_inputs=3,
        verbose=True, enable_training=False
    )
    car = RCCar()
    sensors = SensorClient()

    input("Ready to roll! Press any key to go.")

    for i in range(500):
        readings = sensors.get_readings()
        readings = np.array([readings])
        action = pb.get_action(readings)
        car.step(action)

        print(readings)
        print("Doing action %d." % action)
        print("-"*80)

        if car.proximity_alert(readings):
            print('Crashed!')

    car.cleanup_gpio()
