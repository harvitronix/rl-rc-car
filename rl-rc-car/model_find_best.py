"""
Silly utility for finding the "best" model for a purpose.
"""
import sys
from becho import becho, bechonet
from sim import carmunk
from os import listdir
from os.path import isfile, join

frames = 25000
inputs = 32
actions = 3

# Just change these.
visualize = False
enable_training = False
load_weights = True
save_weights = False
map_style = 'linear'
weights_path = 'saved-models'

# Get weight files.
onlyfiles = [f for f in listdir(weights_path) if isfile(join(weights_path, f))]
onlyfiles = [f for f in onlyfiles if 'h5' in f]

for f in onlyfiles:

    # Get our network and stuff.
    weights_file = weights_path + '/' + f
    try:
        network = bechonet.BechoNet(num_actions=actions, num_inputs=inputs,
                                    nodes_1=50, nodes_2=50, verbose=False,
                                    load_weights=weights_file,
                                    weights_file=weights_file,
                                    save_weights=save_weights)
        pb = becho.ProjectBecho(network, frames=frames, num_actions=actions,
                                batch_size=32, min_epsilon=0.1,
                                num_inputs=inputs, replay_size=10000,
                                gamma=0.99, verbose=False,
                                enable_training=enable_training,
                                save_steps=250)
    except:
        print("Found a weights file that doesn't fit this network.")
        print(weights_file)
        continue

    game_state = carmunk.GameState(noisey=False, map_style=map_style)
    _, state = game_state.frame_step((2))

    distance = 0
    xs = []

    while True:
        # If it made it past everything...
        if len(xs) > 0 and max(xs) > 1000:
            print('-'*80)
            print("%s made it in %d frames." % (f, distance))
            print('-'*80)
            break

        distance += 1
        action = pb.get_action(state)

        reward, state = game_state.frame_step(action)

        # Keep track of the furthest right it makes it.
        car_coords = game_state.get_car_coords()
        xs.append(car_coords[0])

        # When it crashes, it didn't make it.
        if reward == -500:
            print("%s died at %d" % (f, distance))
            break
