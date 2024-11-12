import pygame
from src.entities.sprite import TileSprite

class Wall:
    def __init__(self, x, y, width, height, image_path=None, rows=1, cols=1):
        # Creating an instance of TileSprite instead of inheriting it
        self.sprite = TileSprite(x, y, width, height, image_path, rows, cols)

    def draw(self, screen, player_rect):
        offset_x = screen.get_width() // 2 - player_rect.centerx
        offset_y = screen.get_height() // 2 - player_rect.centery

        # Adjust the wall's position based on the calculated offset
        screen_pos = (self.sprite.rect.x + offset_x, self.sprite.rect.y + offset_y)

        # Draw the wall tile at the calculated position
        if self.sprite.tiles:
            screen.blit(self.sprite.tiles[self.sprite.current_tile_index], screen_pos)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (screen_pos[0], screen_pos[1], self.sprite.rect.width, self.sprite.rect.height))
