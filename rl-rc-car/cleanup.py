from rccar import RCCar
from sensors import Sensors

car = RCCar()
car.cleanup_gpio()

sensors = Sensors()
sensors.cleanup_gpio()
