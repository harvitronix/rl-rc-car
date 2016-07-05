from becho import becho, bechonet
from sim import carmunk
from statistics import mean
import csv

# frames = 10000
frames = 10000
inputs = 5
actions = 6

# Just change these.
train = True
weights_file = 'saved-models/sonar-and-ir-and-prox.h5'

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
                        replay_size=100000, gamma=0.99, verbose=True,
                        enable_training=enable_training,
                        save_steps=750)

rewards = []
distances = []
results = []
distance = 0

repeat_action = 3

game_state = carmunk.GameState(noisey=False)
_, state = game_state.frame_step((2))

for i in range(frames):

    distance += 1
    action = pb.get_action(state)

    # print(state, action)
    # input("Press enter.")

    for x in range(repeat_action):
        reward, new_state = game_state.frame_step(action)

    if enable_training:
        pb.step(state, action, reward, new_state, False)

    # Mimic terminal for reporting.
    if reward == -10:
        print("Proximity alert at frame %d." % i)
        # Give us some info.
        distances.append(distance)
        if len(distances) > 25:
            distances.pop(0)
        results.append(mean(distances))
        distance = 0

    state = new_state

    # Every 100 frames, if we've crashed (so we have something to show)...
    if i % 100 == 0 and i > 0 and len(distances) > 0:
        print("%d - Average distance: %.2f" % (i, mean(distances)))
        print("Epsilon: %.5f" % pb.epsilon)

# Save stuff.
with open('results/loss-log.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(network.loss_log)
