"""
This is used to gather our readings from the remote sensor server.
http://ilab.cs.byu.edu/python/socket/echoclient.html
"""

import socket
import time
import json
from vis import visualize_polar, visualize_sensors


class SensorClient:
    def __init__(self, host, port=8888, size=1024):
        self.host = host
        self.port = port
        self.size = size

    def get_readings(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        readings = s.recv(self.size)
        s.close()

        # Decode the response into a dictionary.
        readings = json.loads(readings.decode('utf-8'))

        # Now return our data the way our NN expects it.
        # We separate out the proximity sensors because those are just
        # used to turn the car around. We concat the sonar array
        # with our middle sonar to build the actual state.
        return_dict = {
            'ir_l': readings['ir_l'],
            'ir_r': readings['ir_r'],
            'state': readings['ir_s'] + [readings['s_m']]
        }
        return return_dict


if __name__ == '__main__':
    # Testing it out.
    from becho import becho, bechonet
    import numpy as np

    inputs = 32
    actions = 3

    network = bechonet.BechoNet(
        num_actions=actions, num_inputs=inputs,
        nodes_1=50, nodes_2=50, verbose=True,
        load_weights=True,
        weights_file='saved-models/servo-332900.h5')
    pb = becho.ProjectBecho(
        network, num_actions=actions, num_inputs=inputs,
        verbose=True, enable_training=False)
    sensors = SensorClient(host='192.168.2.10')

    while True:
        # Get the reading.
        try:
            readings = sensors.get_readings()
            proximity = True if readings['ir_l'] == 0 or \
                readings['ir_r'] == 0 else False
            state = np.array([readings['state']])

            # Visualize our distances.
            visualize_polar(state)

            # Get the action.
            action = pb.get_action(state)
            print("Doing action %d" % action)
        except:
            print("Error getting readings.")
            raise
