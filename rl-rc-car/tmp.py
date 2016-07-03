from becho import becho, bechonet
import numpy as np

inputs = 3
actions = 6
frames = 1000

# Just change these.
train = False
weights_file = 'saved-models/sonar-and-ir.h5'

if train:
    enable_training = True
    load_weights = False
    save_weights = True
else:
    enable_training = False
    load_weights = True
    save_weights = False

network = bechonet.BechoNet(num_actions=actions, num_inputs=inputs,
                            nodes_1=256, nodes_2=256, verbose=True,
                            load_weights=load_weights,
                            weights_file=weights_file,
                            save_weights=save_weights)
pb = becho.ProjectBecho(network, frames=frames, num_actions=actions,
                        batch_size=50, min_epsilon=0.1, num_inputs=inputs,
                        replay_size=100000, gamma=0.9, verbose=True,
                        enable_training=enable_training,
                        save_steps=750)

while True:
    distance = input("Enter distance: ")
    state = [1, distance, 1]
    state = np.array([state])
    action = pb.get_action(state.astype(int))
    print(state.astype(int), action)
