from becho import becho, bechonet
from sim import carmunk
from statistics import mean


if __name__ == "__main__":
    frames = 2000
    inputs = 3
    actions = 3

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
                                nodes_1=512, nodes_2=512, verbose=True,
                                load_weights=load_weights,
                                weights_file=weights_file,
                                save_weights=save_weights)
    pb = becho.ProjectBecho(network, frames=frames, num_actions=actions,
                            batch_size=32, min_epsilon=0.1, num_inputs=inputs,
                            replay_size=1000000, gamma=0.99, verbose=True,
                            enable_training=enable_training,
                            save_steps=500)

    rewards = []
    results = []
    max_steps = 2000
    repeat_action = 2

    game_state = carmunk.GameState()

    distances = []
    results = []

    distance = 0

    _, state = game_state.frame_step((2))

    for i in range(frames):

        distance += 1
        action = pb.get_action(state)

        reward, new_state = game_state.frame_step(action)

        if reward == -500:
            # Give us some info.
            print(distance)
            distances.append(distance)
            if len(distances) > 5:
                distances.pop(0)
            distance = 0

        pb.step(state, action, reward, new_state, False)

        state = new_state

        if i % 100 == 0 and i > 0:
            print("Epsilon: %.5f" % pb.epsilon)
            print("%d - Average distance: %.2f" % (i, mean(distances)))
            results.append(mean(distances))

    for r in results:
        print(r)
