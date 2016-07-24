"""
Small utility for resetting the remote control because it gets stuck sending
signals sometimes after killing the process.
"""
from rccar import RCCar

car = RCCar()
car.cleanup_gpio()
