from src.entities.sprite import StaticSprite

class Door():
    def __init__(self, x, y, width, height, filepath):
        self.sprite = StaticSprite(x, y, width, height, filepath)
        self.open = False
        self.sprite.load_image(filepath)

    def draw(self, screen, player_rect):
        # Calculate the door's position with the offset applied for rendering
        offset_x = screen.get_width() // 2 - player_rect.centerx
        offset_y = screen.get_height() // 2 - player_rect.centery

        # Adjust the door's position based on the calculated offset
        screen_pos = (self.sprite.rect.x + offset_x, self.sprite.rect.y + offset_y)
        screen.blit(self.sprite.image, screen_pos)

