"""
A module for simulating sensors of different types. This is way too hard-coded
and not real OOP, but it's better than having it within carmunk for now.
"""
import random
import math
from pygame.color import THECOLORS


class Sensors:
    """Make the sensors we need. This is basically hard-coded for now."""
    def __init__(self, x, y, angle, width,
                 height, screen, pygame, noisey=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.pygame = pygame
        self.angle = angle
        self.noisey = noisey
        self.sensors = {
            'l_p': {'angle_diff': 0.75, 'type': 'prox', 'reading:': None},
            'r_p': {'angle_diff': -0.75, 'type': 'prox', 'reading:': None},
            #'l_d': {'angle_diff': 0.5, 'type': 'sonar', 'reading:': None},
            #'r_d': {'angle_diff': -0.5, 'type': 'sonar', 'reading:': None},
            'm_s': {'angle_diff': 0, 'type': 'sonar', 'reading:': None},
        }
        self.arm = self.make_sensor_arm(self.x, self.y)

    def set_readings(self):
        for key, value in self.sensors.items():
            reading = self.get_sensor_reading(
                self.arm, self.x, self.y, self.angle,
                value['angle_diff'],
                value['type']
            )

            if self.noisey and value['type'] == 'sonar':
                reading = self.make_sonar_noise(reading)

            self.sensors[key]['reading'] = reading

        return self.sensors

    def get_readings(self):
        """
        Makes a usable "state". Hard coded. :(
        """
        state = []
        #s_order = ['l_p', 'l_d', 'm_s', 'r_d', 'r_p']
        s_order = ['l_p', 'm_s', 'r_p']
        for i in s_order:
            state.append(self.sensors[i]['reading'])
        return state

    def proximity_alert(self):
        for r in self.readings:
            if r < 1:
                return True
        else:
            return False

    def make_sonar_noise(self, reading):
        """
        This attemts to mimic noisey sensors. Because sonar is noisey.

        70% of the time, just return a random reading.
        """
        if random.randint(0, 10) > 7:
            new_reading = random.randint(0, 39)
        else:
            new_reading = reading

        return new_reading

    def get_sensor_reading(self, arm, x, y, angle, offset, s_type='sonar'):
        """
        We use this same method for both IR and sonar. Sonar returns a distance
        while IR just returns a 0 or 1 depending on if it detected something.
        For sonar, 1 = didn't detect anything, 0 = detected something.
        """
        if s_type == 'sonar':
            sonar = True
        else:
            sonar = False

        # Used to count the distance.
        i = 0
        max_sonar_distance = 5

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            if not sonar and i > max_sonar_distance:
                break

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= self.width \
                    or rotated_p[1] >= self.height:
                break  # Distance is the current i.
            else:
                obs = self.screen.get_at(rotated_p)
                if self.get_track_or_not(obs) != 0:
                    break  # Distance is the current i.

            self.pygame.draw.circle(
                self.screen, (255, 255, 255), (rotated_p), 2)

        # Depending on if it's sonar or IR, we return different values.
        if sonar:
            return i * 5  # Try to get the value closer to reality.
        else:
            # It's IR.
            if i <= max_sonar_distance:
                return 0
            else:
                return 1

    def make_sensor_arm(self, x, y):
        spread = 8  # Default spread.
        distance = 18  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))

        return arm_points

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = self.height - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading):
        if reading == THECOLORS['black']:
            return 0
        else:
            return 1
