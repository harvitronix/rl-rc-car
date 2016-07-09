import random
import numpy as np
from sim import sensors

import pygame
from pygame.color import THECOLORS

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw

# PyGame init
width = 1200
height = 650
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Turn off alpha since we don't use it.
screen.set_alpha(None)

# Showing sensors and redrawing slows things down.
show_sensors = True
draw_screen = True


class GameState:
    def __init__(self, noisey=False):
        # Noisey sensors?
        self.noisey = noisey

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)

        # Create the car.
        self.create_car(100, 100, -0.75)
        self.driving_direction = 0

        # Record steps.
        self.num_steps = 0

        # Create outer walls.
        static = [
            pymunk.Segment(
                self.space.static_body,
                (0, 1), (0, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, height), (width, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (width-1, height), (width-1, 1), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, 1), (width, 1), 1)
        ]
        for s in static:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
            s.color = THECOLORS['red']
        self.space.add(static)

        # Create some inner "walls".
        self.create_circle_box(200, 125, 400, 400)
        self.create_circle_box(0, 525, 800, 650)
        self.create_circle_box(600, 300, 700, 550)
        self.create_circle_box(550, 0, 1000, 150)
        self.create_circle_box(850, 275, 1075, 450)

        # Create a cat.
        self.create_cat()

        # Initialize our sensors.
        self.sensor_obj = sensors.Sensors(width, height, screen, pygame, False)

    def create_circle_box(self, x1, y1, x2, y2):
        """
        Create a box out of circles. We do this ridiculousness because
        for the life of me I can't figure out how to make a simple box!
        """
        # Defaults.
        radius = 15
        gap = 0

        # Calculated values.
        circumference = radius * 2
        width = x2 - x1
        height = y2 - y1
        cols = int(width / (circumference + gap))
        rows = int(height / (circumference + gap))

        # Build a bunch of circles.
        for y in range(rows):
            for x in range(cols):
                space_x = x1 + (x * (circumference + gap))
                space_y = y1 + (y * (circumference + gap))
                self.create_obstacle(space_x, space_y, radius)

    def create_obstacle(self, x, y, r):
        c_body = pymunk.Body(pymunk.inf, pymunk.inf)
        c_shape = pymunk.Circle(c_body, r)
        c_shape.elasticity = 1.0
        c_body.position = x, y
        c_shape.color = THECOLORS["blue"]
        self.space.add(c_body, c_shape)
        return c_body

    def create_cat(self):
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.cat_body = pymunk.Body(1, inertia)
        self.cat_body.position = 800, 200
        self.cat_shape = pymunk.Circle(self.cat_body, 30)
        self.cat_shape.color = THECOLORS["orange"]
        self.car_shape.elasticity = 1.0
        self.cat_shape.angle = 0.5
        self.space.add(self.cat_body, self.cat_shape)

    def create_car(self, x, y, r):
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = x, y
        self.car_shape = pymunk.Circle(self.car_body, 15)
        self.car_shape.color = THECOLORS["green"]
        self.car_shape.elasticity = 1.0
        self.car_body.angle = r
        self.driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.apply_impulse(self.driving_direction)
        self.space.add(self.car_body, self.car_shape)

    def frame_step(self, action):
        # Move cat.
        if self.num_steps % 5 == 0:
            self.move_cat()

        # Turning.
        turning = False
        if action == 0:  # Turn right.
            self.car_body.angle -= .05
            turning = True
        elif action == 1:  # Turn left.
            self.car_body.angle += .05
            turning = True

        self.driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.velocity = 50 * self.driving_direction

        # Update the screen and stuff.
        screen.fill(THECOLORS["black"])
        draw(screen, self.space)
        self.space.step(1./10)
        if draw_screen:
            pygame.display.flip()
        clock.tick()

        # Get the current location and the readings there.
        x, y = self.car_body.position

        # Set and get our sensor readings.
        self.sensor_obj.set_readings(x, y, self.car_body.angle)

        # Get readings.
        proximity_sensors = self.sensor_obj.get_readings()

        # The 3rd list item is the middle sonar.
        forward_sonar = proximity_sensors[2]

        # Now set the proximity sensors.
        proximity_sensors = proximity_sensors[0:2]

        # Get the sonar sweep reading.
        sonar_sweep = self.sensor_obj.get_sonar_sweep_readings()

        state = sonar_sweep + [forward_sonar]

        # Set the reward.
        reward = self.get_reward(proximity_sensors, turning)

        # Show sensors.
        pygame.display.update()

        # Numpy it.
        state = np.array([state])

        self.num_steps += 1

        return reward, state

    def get_reward(self, readings, turning):
        if readings[0] == 0 or readings[1] == 0:
            # One of our front-facing sensors is very close to something.
            reward = -500
        elif turning:
            # Less reward if turning.
            reward = 0
        else:
            # We're going straight.
            reward = 1

        return reward

    def move_cat(self):
        speed = random.randint(50, 120)
        self.cat_body.angle -= random.randint(-1, 1)
        direction = Vec2d(1, 0).rotated(self.cat_body.angle)
        self.cat_body.velocity = speed * direction

    def recover(self):
        self.car_body.velocity = -100 * self.driving_direction
        for i in range(4):
            if random.randint(0, 1) == 0:
                self.car_body.angle += .2  # Turn a little.
            else:
                self.car_body.angle -= .2  # Turn a little.
            screen.fill(THECOLORS["black"])
            draw(screen, self.space)
            self.space.step(1./10)
            if draw_screen:
                pygame.display.flip()
            clock.tick()


if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 2)))
