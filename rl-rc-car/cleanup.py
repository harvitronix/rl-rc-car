from rccar import RCCar
from sensors import Sensors

car = RCCar()
car.cleanup_gpio()

ir_pins = [24, 21]
sonar_pins = [[25, 8]]
sensors = Sensors(ir_pins, sonar_pins)
sensors.cleanup_gpio()
