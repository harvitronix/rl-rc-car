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
        with open('readings.json') as f:
            try:
                data = json.load(f)
            except:
                print("Got bad JSON data from file. Not sending.")
                return False

        client, address = self.s.accept()
        print("Sending: %s" % str(data))
        b = json.dumps(data).encode('utf-8')
        client.sendall(b)
        client.close()
        return True


if __name__ == '__main__':
    input("Start sensors.py in the background then hit enter to start server.")
    ss = SensorServer()
    while 1:
        ss.serve_readings()
