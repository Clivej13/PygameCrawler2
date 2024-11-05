import pygame
from sprite import StaticSprite

class Door(StaticSprite):
    def __init__(self, x, y, width, height, filepath):
        super().__init__(x, y, width, height, filepath)
        self.open = False
        self.load_image(filepath)

    def draw(self, screen, player_rect):
        # Calculate the door's position with the offset applied for rendering
        offset_x = screen.get_width() // 2 - player_rect.centerx
        offset_y = screen.get_height() // 2 - player_rect.centery

        # Adjust the door's position based on the calculated offset
        screen_pos = (self.rect.x + offset_x, self.rect.y + offset_y)
        screen.blit(self.image, screen_pos)

