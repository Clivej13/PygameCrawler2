import pygame
from src.entities.sprite import TileSprite

class Floor:
    def __init__(self, x, y, width, height, image_path=None, rows=1, cols=1):
        # Creating an instance of TileSprite instead of inheriting it
        self.sprite = TileSprite(x, y, width, height, image_path, rows, cols)

    def update(self, delta_time):
        # No need to modify rect.x or rect.y with offset values here
        pass

    def draw(self, screen, player_rect):
        offset_x = screen.get_width() // 2 - player_rect.centerx
        offset_y = screen.get_height() // 2 - player_rect.centery

        # Adjust the floor tile position based on the calculated offset
        screen_pos = (self.sprite.rect.x + offset_x, self.sprite.rect.y + offset_y)

        # Use the TileSprite instance to draw at the calculated position
        if self.sprite.tiles:
            screen.blit(self.sprite.tiles[self.sprite.current_tile_index], screen_pos)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (screen_pos[0], screen_pos[1], self.sprite.rect.width, self.sprite.rect.height))
