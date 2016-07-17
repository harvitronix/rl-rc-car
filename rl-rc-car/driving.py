"""
This is the real-world equivalent of the simulation's learning.py.
"""
from becho import becho, bechonet
from rccar import RCCar
from sensor_client import SensorClient
import numpy as np
import csv


def get_reward_from_sensors(car, readings, action):
    if car.proximity_alert(readings):
        # If one of our sensors touches something...
        reward = -10
    elif action > 2:
        # If we're going backwards, give negative reward.
        reward = -2
    elif action == 0 or action == 1:
        # Less reward if turning.
        reward = 1
    else:
        # We're going straight.
        reward = 2

    return reward


if __name__ == '__main__':
    train = False
    weights_file = 'saved-models/servo-332900.h5'

    inputs = 32
    actions = 3

    if train:
        enable_training = True
        load_weights = False
        save_weights = True
    else:
        enable_training = False
        load_weights = True
        save_weights = False

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
    car = RCCar(apply_time=0.2, wait_time=0.4)
    sensors = SensorClient()

    input("Ready to roll! Press any key to go.")

    # Get initial state.
    state = sensors.get_readings()
    state = np.array([state])

    for i in range(500):
        # Get action.
        action = pb.get_action(state)

        print(state, action)
        input("Press enter.")

        # Take action.
        car.step(action)

        # Get new readings.
        new_state = sensors.get_readings()
        new_state = np.array([new_state])

        if enable_training:
            # Get reward.
            reward = get_reward_from_sensors(car, new_state, action)

            # Train.
            pb.step(state, action, reward, new_state, False)

        # Override state.
        state = new_state

        if car.proximity_alert(state):
            print('Proximity alert!')
            car.recover()

        print("-"*80)

    car.cleanup_gpio()

    if enable_training:
        # Save stuff.
        with open('results/realcar-loss-log.csv', 'w') as myfile:
            wr = csv.writer(myfile)
            wr.writerows(network.loss_log)
