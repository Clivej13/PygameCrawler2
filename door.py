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

        # Calculate the expanded rect and adjust its position for rendering
        expanded_rect = self.expand_rect()
        expanded_rect_screen_pos = expanded_rect.move(offset_x, offset_y)

        # Draw the expanded collision rectangle for debugging purposes
        pygame.draw.rect(screen, (0, 255, 0), expanded_rect_screen_pos, 1)  # Draw the rect with a green outline, width of 1 pixel

    def expand_rect(self):
        # Expand the rect by double in all four directions
        new_rect = pygame.Rect(
            self.rect.x - self.rect.width // 2,
            self.rect.y - self.rect.height // 2,
            self.rect.width * 2,
            self.rect.height * 2
        )
        return new_rect
