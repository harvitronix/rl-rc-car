"""
This runs continuously and serves our sensor readings when requested.

Base script from:
http://ilab.cs.byu.edu/python/socket/echoserver.html
"""

import socket
from sensors import Sensors


class SensorServer:
    def __init__(self, host='', port=8888, size=1024, backlog=5):
        self.host = host
        self.port = port
        self.size = size
        self.backlog = backlog

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(backlog)

    def serve_readings(self, sensors):
        client, address = self.s.accept()
        data = str(sensors.get_all_readings())
        try:
            print("Sending: %s" % str(data))
            client.send(data.encode(encoding='utf_8'))
        except:
            print("Couldn't send data.")
        client.close()


if __name__ == '__main__':
    # Input pins.
    ir_pins = [24, 21]
    sonar_pins = [[25, 8]]

    # Get objects.
    sensors = Sensors(ir_pins, sonar_pins)
    ss = SensorServer()

    while 1:
        ss.serve_readings(sensors)

    sensors.cleanup_gpio()
