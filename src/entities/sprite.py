import pygame
import os
import random

from src.utilities.file_manager import FileManager


# Base Sprite Class
class BaseSprite:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = None

    def load_image(self, filename):
        """Load image directly in the class and store it as an attribute."""
        self.image = FileManager.load_image(filename)

    def draw(self, screen):
        raise NotImplementedError("Subclasses must implement draw() method.")


# Static Sprite Class
class StaticSprite(BaseSprite):
    def __init__(self, x, y, width, height, filepath=None):
        super().__init__(x, y, width, height)
        if filepath:
            self.load_image(filepath)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)


# Animated Sprite Class
class AnimatedSprite(BaseSprite):
    def __init__(self, x, y, width, height, animation_paths=None):
        super().__init__(x, y, width, height)
        self.animation_images = []
        self.animation_index = 0
        self.frame_count = 0
        if animation_paths:
            self.load_animation_images(animation_paths)

    def load_animation_images(self, animation_paths):
        """Load all images for animation and store them in a list."""
        for path in animation_paths:
            if os.path.exists(path):
                try:
                    image = pygame.image.load(path).convert_alpha()
                    self.animation_images.append(image)
                except pygame.error as e:
                    print(f"Error loading animation image {path}: {e}")

    def draw(self, screen):
        if self.animation_images:
            animation_frame = self.animation_images[self.animation_index]
            screen.blit(animation_frame, self.rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def animate(self, speed=18):
        if self.animation_images:
            self.frame_count += 1
            if self.frame_count >= speed:
                self.frame_count = 0
                self.animation_index = (self.animation_index + 1) % len(self.animation_images)


# Tile Sprite Class
class TileSprite(BaseSprite):
    def __init__(self, x, y, width, height, image_path=None, rows=1, cols=1):
        super().__init__(x, y, width, height)
        self.tiles = []
        self.current_tile_index = 0
        if image_path:
            self.load_image(image_path)
            self.prepare_tiles(rows, cols)
            self.select_random_tile()

    def prepare_tiles(self, rows, cols):
        """Cut the loaded image into tiles and store them."""
        if self.image:
            tile_width = self.image.get_width() // cols
            tile_height = self.image.get_height() // rows
            for i in range(rows):
                for j in range(cols):
                    tile_rect = pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height)
                    self.tiles.append(self.image.subsurface(tile_rect))

    def draw(self, screen):
        if self.tiles:
            screen.blit(self.tiles[self.current_tile_index], self.rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def select_random_tile(self):
        if self.tiles:
            self.current_tile_index = random.randint(0, len(self.tiles) - 1)
