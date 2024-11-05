import pygame
import math

class AttackDirectionIndicator:
    def __init__(self, screen_width, screen_height, distance=50, radius=5, color=(255, 255, 0)):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.distance = distance  # Distance from the player at which the circle will orbit
        self.radius = radius  # Radius of the circle
        self.color = color  # Color of the circle

        # Initialize the circle position to the player's center initially
        self.circle_x = self.screen_width // 2
        self.circle_y = self.screen_height // 2

        # Create a rect to represent the collision area
        self.rect = pygame.Rect(self.circle_x - self.radius, self.circle_y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        # Get the center of the player (on the screen)
        screen_center = (self.screen_width // 2, self.screen_height // 2)

        # Get the mouse position on the screen
        mouse_pos = pygame.mouse.get_pos()

        # Calculate the angle between the player center and mouse position
        delta_x = mouse_pos[0] - screen_center[0]
        delta_y = mouse_pos[1] - screen_center[1]
        angle = math.atan2(delta_y, delta_x)

        # Calculate the new position of the circle using trigonometry, relative to the player's screen center
        self.circle_x = screen_center[0] + math.cos(angle) * self.distance
        self.circle_y = screen_center[1] + math.sin(angle) * self.distance

        # Update the rect position to match the new circle position
        self.rect.x = self.circle_x - self.radius
        self.rect.y = self.circle_y - self.radius

    def draw(self, screen):
        # Draw the circle at the calculated position
        pygame.draw.circle(screen, self.color, (int(self.circle_x), int(self.circle_y)), self.radius)
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)  # Draw the rect with a green outline, width of 1 pixel
