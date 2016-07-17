"""
This runs continuously and serves our sensor readings when requested.

Base script from:
http://ilab.cs.byu.edu/python/socket/echoserver.html
"""
import redis
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

        self.r_server = redis.Redis('localhost')

    def serve_readings(self):
        ir_s = self.r_server.get('ir_s').decode('utf-8')
        ir_l = self.r_server.get('ir_l').decode('utf-8')
        ir_r = self.r_server.get('ir_r').decode('utf-8')
        s_m = json.loads(self.r_server.get('s_m').decode('utf-8'))

        readings = {
            'ir_s': ir_s,
            'ir_l': ir_l,
            'ir_r': ir_r,
            's_m': s_m
        }
        print(readings)
        client, address = self.s.accept()
        print("Sending: %s" % str(readings))
        b = json.dumps(readings).encode('utf-8')
        client.sendall(b)
        client.close()


if __name__ == '__main__':
    input("Start sensor_run.py then hit enter to start server.")
    ss = SensorServer()
    while 1:
        ss.serve_readings()
