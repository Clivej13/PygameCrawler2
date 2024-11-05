# In sprite.py

import math
import pygame

from sprite import AnimatedSprite


class Fireball(AnimatedSprite):
    def __init__(self, x, y, width, height, angle, speed=300, animation_paths=None):
        super().__init__(x, y, width, height, animation_paths)
        self.angle = angle
        self.speed = speed
        self.velocity_x = math.cos(self.angle) * self.speed
        self.velocity_y = math.sin(self.angle) * self.speed

    def update(self, delta_time):
        # Move the fireball based on its speed and direction
        self.rect.x += self.velocity_x * delta_time
        self.rect.y += self.velocity_y * delta_time
        # Update the animation frame
        self.animate()
