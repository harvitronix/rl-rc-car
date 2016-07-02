"""
Just used to test our server.
http://ilab.cs.byu.edu/python/socket/echoclient.html
"""

from becho import becho, bechonet
import socket
import numpy as np
import time

HOST = '192.168.2.9'
PORT = 8888
SIZE = 1024

network = bechonet.BechoNet(num_actions=6, num_inputs=4,
                            nodes_1=256, nodes_2=256, verbose=True,
                            load_weights=True,
                            weights_file='saved-models/sonar-and-ir-4500.h5')
pb = becho.ProjectBecho(network, num_actions=6, num_inputs=4,
                        verbose=True, enable_training=False)

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))
    readings = s.recv(SIZE)
    s.close()

    # Turn our weird stringed list into an actual list.
    readings = readings.decode('utf-8')
    readings = readings[1:-1]
    readings = readings.split(', ')
    readings = [float(i) for i in readings]

    # Assume we're going forward.
    readings.append(1)

    # Numpy it.
    readings = np.array([readings])
    print(readings)

    # Get the action.
    action = pb.get_action(readings)
    print("Doing action %d" % action)

    time.sleep(0.5)
