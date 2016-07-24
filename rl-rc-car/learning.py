from becho import becho, bechonet
from sim import carmunk
import csv
from vis import visualize_polar
from statistics import mean
import seaborn as sns
import matplotlib.pyplot as plt
import timeit

frames = 100000
inputs = 32
actions = 3

# Just change these.
train = False
weights_file = 'saved-models/nix-try-99700.h5'
visualize = False

if train:
    enable_training = True
    load_weights = False
    save_weights = True
    map_style = 'default'
else:
    enable_training = False
    load_weights = True
    save_weights = False
    map_style = 'linear'

network = bechonet.BechoNet(num_actions=actions, num_inputs=inputs,
                            nodes_1=164, nodes_2=150, verbose=True,
                            load_weights=load_weights,
                            weights_file=weights_file,
                            save_weights=save_weights)
pb = becho.ProjectBecho(network, frames=frames, num_actions=actions,
                        batch_size=32, min_epsilon=0.1, num_inputs=inputs,
                        replay_size=10000, gamma=0.99, verbose=True,
                        enable_training=enable_training,
                        save_steps=250)

rewards = []
distances = []
results = []
distance = 0
repeat_action = 1
losses = []

game_state = carmunk.GameState(noisey=False, map_style=map_style)
_, state = game_state.frame_step((2))

# Time it.
start_time = timeit.default_timer()

for i in range(frames):
    terminal = False
    distance += 1
    action = pb.get_action(state)

    # Let's see what the robocar sees.
    if visualize:
        print(state)
        visualize_polar(state)

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

        # Print our recent loss.
        new_ll = []
        if len(network.loss_log) > 50:
            # There has to be a better way to do this...
            for ll in network.loss_log:
                new_ll.append(ll[0].tolist())
            mean_loss = mean(new_ll)
            print("Mean loss, last 50 frames: %f" %
                  (mean_loss))
            losses.append(mean_loss)

            # Plotting.
            sns.plt.clf()
            sns.set_style("darkgrid")
            plt.plot(losses)
            sns.plt.draw()
            sns.plt.pause(0.05)

            # Timing.
            batch_time = timeit.default_timer() - start_time
            print("Time per frame: %f" % (batch_time / 100))
            start_time = timeit.default_timer()

        # Update the save filename so we can look at different points.
        new_ending = '-' + str(i) + '.h5'
        network.weights_file = weights_file.replace(".h5", new_ending)

# Keep the plot open.
sns.plt.show()

# Save stuff.
with open('results/loss-log.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerows(network.loss_log)

# Save again.
new_ending = '-' + str(i) + '.h5'
network.weights_file = weights_file.replace(".h5", new_ending)
