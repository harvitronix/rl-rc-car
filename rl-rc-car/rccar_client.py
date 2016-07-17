"""
Send commands to the car.
"""
import socket


class RCCarClient:
    def __init__(self, host, port=8888, size=1024):
        self.host = host
        self.port = port
        self.size = size

    def send_message(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(message.encode())
        s.close()

    def cleanup_gpio(self):
        self.send_message('cleanup_gpio')

    def step(self, action):
        self.send_message('step-' + str(action))

    def recover(self):
        self.send_message('recover')


if __name__ == '__main__':
    # For testing.
    rccar_client = RCCarClient(host='192.168.2.9')
    rccar_client.cleanup_gpio()
