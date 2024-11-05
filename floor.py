import pygame
from sprite import TileSprite


class Floor(TileSprite):
    def __init__(self, x, y, width, height, image_path=None, rows=1, cols=1):
        super().__init__(x, y, width, height, image_path, rows, cols)

    def update(self, delta_time):
        # No need to modify rect.x or rect.y with offset values here
        pass

    def draw(self, screen, player_rect):
        offset_x = screen.get_width() // 2 - player_rect.centerx
        offset_y = screen.get_height() // 2 - player_rect.centery

        # Adjust the enemy's position based on the calculated offset
        screen_pos = (self.rect.x + offset_x, self.rect.y + offset_y)

        # Draw the floor tile at the calculated position
        if self.tiles:
            screen.blit(self.tiles[self.current_tile_index], screen_pos)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (screen_pos[0], screen_pos[1], self.rect.width, self.rect.height))
