import pygame
import math
from sprite import StaticSprite


class AttackDirectionIndicator:
    def __init__(self, screen_width, screen_height, distance=50, width=10, height=10, color=(255, 255, 0), filepath=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.distance = distance  # Distance from the player at which the rect will orbit
        self.width = width  # Width of the rect
        self.height = height  # Height of the rect
        self.color = color  # Color of the rect

        # Initialize the rect position to the player's center initially
        self.rect_x = self.screen_width // 2
        self.rect_y = self.screen_height // 2

        # Create a StaticSprite for managing the visual representation of the weapon
        self.sprite = StaticSprite(self.rect_x - self.width // 2, self.rect_y - self.height // 2, self.width, self.height, filepath)

        # Store the original image to enable proper rotation
        if self.sprite.image:
            self.original_image = self.sprite.image

    def update(self):
        # Get the center of the player (on the screen)
        screen_center = (self.screen_width // 2, self.screen_height // 2)

        # Get the mouse position on the screen
        mouse_pos = pygame.mouse.get_pos()

        # Calculate the angle between the player center and mouse position
        delta_x = mouse_pos[0] - screen_center[0]
        delta_y = mouse_pos[1] - screen_center[1]
        angle = math.degrees(math.atan2(delta_y, delta_x))

        # Calculate the new position of the sword using trigonometry, relative to the player's screen center
        self.rect_x = screen_center[0] + math.cos(math.radians(angle)) * self.distance
        self.rect_y = screen_center[1] + math.sin(math.radians(angle)) * self.distance

        # Update the sprite's rect position to match the new calculated position
        self.sprite.rect.x = self.rect_x - self.width // 2
        self.sprite.rect.y = self.rect_y - self.height // 2

        # Rotate the image
        if self.sprite.image:
            # Rotate the original image by the negative of the angle to point in the correct direction
            self.sprite.image = pygame.transform.rotate(self.original_image, -angle)

            # Adjust the rect to keep the correct center after rotation
            self.sprite.rect = self.sprite.image.get_rect(center=(self.rect_x, self.rect_y))

    def draw(self, screen):
        # Delegate the drawing to the StaticSprite instance
        self.sprite.draw(screen)
