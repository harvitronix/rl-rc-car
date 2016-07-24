"""
Utility to check that our model is behaving how we expect it to.
"""
from becho import becho, bechonet
import numpy as np

inputs = 32
actions = 3

weights_file = 'saved-models/servo-332900.h5'

network = bechonet.BechoNet(num_actions=actions, num_inputs=inputs,
                            nodes_1=256, nodes_2=256, verbose=True,
                            load_weights=True,
                            weights_file=weights_file,
                            save_weights=False)
pb = becho.ProjectBecho(network, num_actions=actions, num_inputs=inputs,
                        verbose=True, enable_training=False)

while True:
    state = input("Enter a state: ")
    state = eval(state)
    state = np.array([state])
    action = pb.get_action(state.astype(int))
    print(action)
