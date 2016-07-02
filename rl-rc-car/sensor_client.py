"""
This is used to gather our readings from the remote sensor server.
http://ilab.cs.byu.edu/python/socket/echoclient.html
"""

import socket
import time


class SensorClient:
    def __init__(self, host='192.168.2.9', port=8888, size=1024):
        self.host = host
        self.port = port
        self.size = size

    def get_readings(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        readings = s.recv(self.size)
        s.close()

        # Turn our weird stringed list into an actual list.
        readings = readings.decode('utf-8')
        readings = readings[1:-1]
        readings = readings.split(', ')
        readings = [float(i) for i in readings]

        return readings


if __name__ == '__main__':
    # Testing it out.
    from becho import becho, bechonet
    import numpy as np

    network = bechonet.BechoNet(
        num_actions=6, num_inputs=3,
        nodes_1=256, nodes_2=256, verbose=True,
        load_weights=True,
        weights_file='saved-models/sonar-and-ir-9750.h5')
    pb = becho.ProjectBecho(
        network, num_actions=6, num_inputs=3,
        verbose=True, enable_training=False)
    sensors = SensorClient()

    while True:
        # Get the reading.
        readings = sensors.get_readings()
        readings = np.array([readings])
        print(readings)

        # Get the action.
        action = pb.get_action(readings)
        print("Doing action %d" % action)

        time.sleep(0.5)
