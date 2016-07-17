"""
Send commands to the car.
"""

import socket
import json


class SensorClient:
    def __init__(self, host, port=8888, size=1024):
        self.host = host
        self.port = port
        self.size = size

    def send_action(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        readings = s.recv(self.size)
        s.close()

    def cleanup_gpio(self):
        self.send_action('cleanup_gpi')

    def step(self, action):
        self.send_action('step-' + str(action))

    def recover(self):
        self.send_action('recover')
