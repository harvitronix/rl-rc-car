"""
This is the real-world equivalent of the simulation's learning.py. It's run
from a computer, calling sensor data from the car's Pi and then sending
actions for the remote control Pi to do.
"""
from becho import becho, bechonet
from sensor_client import SensorClient
from rccar_client import RCCarClient
import numpy as np
from vis import visualize_polar


if __name__ == '__main__':
    # Set defaults.
    weights_file = 'saved-models/servo-4400.h5'
    inputs = 32
    actions = 3
    enable_training = True
    load_weights = True
    save_weights = False
    sensor_host = '192.168.2.10'
    car_host = '192.168.2.9'

    # Setup our two servers.
    sensors = SensorClient(host=sensor_host)
    car = RCCarClient(host=car_host)

    # Setup our network.
    network = bechonet.BechoNet(
        num_actions=actions, num_inputs=inputs,
        nodes_1=50, nodes_2=50, verbose=True,
        load_weights=load_weights,
        weights_file=weights_file,
        save_weights=save_weights
    )
    pb = becho.ProjectBecho(
        network, num_actions=actions, num_inputs=inputs,
        verbose=True, enable_training=enable_training,
        batch_size=50, min_epsilon=0.05, epsilon=0.05,
        replay_size=100000, gamma=0.9, save_steps=100
    )

    input("Ready to roll! Press enter to go.")

    # Get initial state.
    readings = sensors.get_readings()
    state = np.array([readings['state']])

    for i in range(500):
        # Get action.
        print("Getting action.")
        action = pb.get_action(state)

        print(state)
        print("Taking action %d" % action)
        visualize_polar(state)
        input("Press enter.")

        # Take action.
        car.step(action)

        # Get new readings.
        new_readings = sensors.get_readings()
        new_state = np.array([new_readings['state']])

        # Override state.
        state = new_state

        # Make sure we aren't about to crash.
        if new_readings['ir_r'] == 0 or new_readings['ir_l'] == 0:
            print('Proximity alert!')
            car.recover()

        print("-"*80)

    car.cleanup_gpio()
