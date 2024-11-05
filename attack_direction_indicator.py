import pygame
import math

class AttackDirectionIndicator:
    def __init__(self, screen_width, screen_height, distance=50, rect_width=10, rect_height=10, color=(255, 255, 0)):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.distance = distance  # Distance from the player at which the rect will orbit
        self.rect_width = rect_width  # Width of the rect
        self.rect_height = rect_height  # Height of the rect
        self.color = color  # Color of the rect

        # Initialize the rect position to the player's center initially
        self.rect_x = self.screen_width // 2
        self.rect_y = self.screen_height // 2

        # Create a rect to represent the indicator area
        self.rect = pygame.Rect(self.rect_x - self.rect_width // 2, self.rect_y - self.rect_height // 2, self.rect_width, self.rect_height)

    def update(self):
        # Get the center of the player (on the screen)
        screen_center = (self.screen_width // 2, self.screen_height // 2)

        # Get the mouse position on the screen
        mouse_pos = pygame.mouse.get_pos()

        # Calculate the angle between the player center and mouse position
        delta_x = mouse_pos[0] - screen_center[0]
        delta_y = mouse_pos[1] - screen_center[1]
        angle = math.atan2(delta_y, delta_x)

        # Calculate the new position of the rect using trigonometry, relative to the player's screen center
        self.rect_x = screen_center[0] + math.cos(angle) * self.distance
        self.rect_y = screen_center[1] + math.sin(angle) * self.distance

        # Update the rect position to match the new calculated position
        self.rect.x = self.rect_x - self.rect_width // 2
        self.rect.y = self.rect_y - self.rect_height // 2

    def draw(self, screen):
        # Draw the rect at the calculated position
        pygame.draw.rect(screen, self.color, self.rect)
