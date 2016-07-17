"""
This lets us connect to the Pi that controls the RCCar. It acts as an
interface to the RCcar class.
"""
import socket
from rccar import RCCar


class RCCarServer:
    def __init__(self, host='', port=8888, size=1024, backlog=5):
        print("Setting up server.")
        self.size = size
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.s.bind((socket.gethostname(), port))
        self.s.bind((host, port))
        self.s.listen(backlog)

        self.car = RCCar(apply_time=0.2, wait_time=0.4)

        print("Ready.")

    def cleanup_gpio(self):
        self.car.cleanup_gpio()

    def step(self, action):
        self.car.step(action)

    def recover(self):
        self.car.recover()


if __name__ == '__main__':
    car_server = RCCarServer()

    while True:
        conn, address = car_server.s.accept()
        data = conn.recv(car_server.size)
        data = data.decode()
        print("Received: %s" data)
        conn.close()

        if 'step' in data:
            action = data.split('-')[1]
            car_server.step(action)
        elif data == 'cleanup_gpio':
            car_server.cleanup_gpio()
        elif data == 'recover':
            car_server.recover()
