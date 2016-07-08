from becho import becho, bechonet
from sim import carmunk
import csv
from vis import visualize_sensors

frames = 20000
inputs = 16
actions = 3

# Just change these.
train = True
weights_file = 'saved-models/servo.h5'
visualize = True

if train:
    enable_training = True
    load_weights = False
    save_weights = True
else:
    enable_training = False
    load_weights = True
    save_weights = False

network = bechonet.BechoNet(num_actions=actions, num_inputs=inputs,
                            nodes_1=1024, nodes_2=1024, verbose=True,
                            load_weights=load_weights,
                            weights_file=weights_file,
                            save_weights=save_weights)
pb = becho.ProjectBecho(network, frames=frames, num_actions=actions,
                        batch_size=100, min_epsilon=0.1, num_inputs=inputs,
                        replay_size=10000, gamma=0.9, verbose=True,
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
    terminal = False
    distance += 1
    action = pb.get_action(state)

    # Let's see what the robocar sees.
    if visualize:
        visualize_sensors(state)

    for x in range(repeat_action):
        reward, new_state = game_state.frame_step(action)

    # Mimic terminal for reporting.
    if reward == -500:
        terminal = True
        game_state.recover()
        print("Proximity alert at frame %d." % i)

    if enable_training:
        pb.step(state, action, reward, new_state, terminal)

    state = new_state

    # Every 100 frames, show us something.
    if i % 100 == 0 and i > 0:
        print("Epsilon: %.5f" % pb.epsilon)

        # Update the save filename so we can look at different points.
        new_ending = '-' + str(i) + '.h5'
        network.weights_file = weights_file.replace(".h5", new_ending)

# Save stuff.
with open('results/loss-log.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(network.loss_log)
