"""
This runs continuously and serves our sensor readings when requested.

Base script from:
http://ilab.cs.byu.edu/python/socket/echoserver.html
"""

import socket
import json


class SensorServer:
    def __init__(self, host='', port=8888, size=1024, backlog=5):
        self.host = host
        self.port = port
        self.size = size
        self.backlog = backlog

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(backlog)

    def serve_readings(self):
        client, address = self.s.accept()
        with open('readings.json') as f:
            data = json.load(f)
        try:
            print("Sending: %s" % str(data))
            client.send(data.encode(encoding='utf_8'))
        except:
            print("Couldn't send data.")
        client.close()


if __name__ == '__main__':
    input("Start sensors.py in the background then hit enter to start server.")
    ss = SensorServer
    while 1:
        ss.serve_readings()
