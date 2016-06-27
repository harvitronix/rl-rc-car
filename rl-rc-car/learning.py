from becho import becho, bechonet
from sim import carmunk
from statistics import mean


if __name__ == "__main__":
    frames = 10000
    inputs = 3
    actions = 6

    # Just change these.
    train_or_show = 'train'
    weights_file = 'saved-models/testing.h5'

    if train_or_show == 'train':
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
                            batch_size=32, min_epsilon=0.1, num_inputs=inputs,
                            replay_size=100000, gamma=0.99, verbose=True,
                            enable_training=enable_training,
                            save_steps=500)

    rewards = []
    distances = []
    results = []
    distance = 0

    repeat_action = 2

    game_state = carmunk.GameState()
    _, state = game_state.frame_step((2))

    for i in range(frames):

        distance += 1
        action = pb.get_action(state)

        for x in range(repeat_action):
            reward, new_state = game_state.frame_step(action)

        if enable_training:
            pb.step(state, action, reward, new_state, False)

        # Mimi terminal for reporting.
        if reward == -500:
            # Give us some info.
            distances.append(distance)
            if len(distances) > 25:
                distances.pop(0)
            results.append(mean(distances))
            distance = 0

        state = new_state

        if i % 100 == 0 and i > 0:
            print("%d - Average distance: %.2f" % (i, mean(distances)))
            print("Epsilon: %.5f" % pb.epsilon)

    for r in results:
        print(r)
