"""
This little diddy serves up the sensor readings when called.

Base script from:
http://ilab.cs.byu.edu/python/socket/echoserver.html
"""

import socket
from sensing import Sensors

host = ''
port = 8888
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

# Input pins.
ir_pins = [24, 21]
sonar_pins = [[25, 8]]

# Get our sensor class.
sensors = Sensors(ir_pins, sonar_pins)

while 1:
    client, address = s.accept()
    data = str(sensors.get_all_readings())
    try:
        print("Sending: %s" % str(data))
        client.send(data.encode(encoding='utf_8'))
    except:
        print("Couldn't send data.")
    client.close()

sensors.cleanup_gpio()
