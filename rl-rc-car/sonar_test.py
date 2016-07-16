from sensors import SonarSensor

if __name__ == '__main__':
    sonar = SonarSensor(25, 8)
    while True:
        # Take readings and store them in a dict.
        print(sonar.get_reading(5, 1000))
        
