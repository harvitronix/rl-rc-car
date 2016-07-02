"""
This is the real-world equivalent of the simulation's learning.py.
"""
from becho import becho, bechonet
from rccar import RCCar

if __name__ == '__main__':
    print("Driving.")
    network = bechonet.BechoNet(num_actions=6, num_inputs=3,
                                nodes_1=256, nodes_2=256, verbose=True,
                                load_weights=True,
                                weights_file='saved-models/sonar-and-ir-4500.h5')
    pb = becho.ProjectBecho(network, num_actions=6, num_inputs=3,
                            verbose=True, enable_training=False)
    car = RCCar()

    input("Net is prepped. Press enter to run.")

    print("Doing loops.")
    for i in range(500):
        car.step(pb.get_action(car.get_readings()))

    car.cleanup_gpio()
