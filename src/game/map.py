import json
import os

import pygame

from src.entities.objects.map_tiles.wall import Wall
from src.entities.objects.map_tiles.floor import Floor
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.objects.map_tiles.door import Door
from src.utilities.file_manager import FileManager


class Map:
    def __init__(self, map_file,item_catalog):
        self.tiles = []
        self.enemies = []
        self.doors = []  # List to store door objects
        self.player = None
        self.collidable_tiles = []  # List to store collidable tiles (walls)
        self.item_catalog = item_catalog

        map_data = FileManager.load_json_file(map_file)

        # Define the size of each tile
        tile_width, tile_height = 50, 50

        # Iterate over the map data and create the appropriate tiles
        for row_idx, row in enumerate(map_data):
            for col_idx, tile_value in enumerate(row):
                x, y = col_idx * tile_width, row_idx * tile_height

                if tile_value == 0:
                    # Create a Floor tile
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "stone_floor.png", 4, 4))
                elif tile_value == 1:
                    # Create the waplayer
                    if not self.player:
                        self.player = Player(x, y, tile_width, tile_height, filepath="adam.png", item_catalog=self.item_catalog)
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "stone_floor.png", 4, 4))
                elif tile_value == 2:
                    wall = Wall(x, y, tile_width, tile_height, "stone_walls_x.png", 2, 7)
                    self.tiles.append(wall)
                    self.collidable_tiles.append(wall)  # Add wall to collidable tiles list
                elif tile_value == 3:
                    # Create a wall tile (horizontal or vertical)
                    wall = Wall(x, y, tile_width, tile_height, "stone_walls_y.png", 2, 2)
                    self.tiles.append(wall)
                    self.collidable_tiles.append(wall)  # Add wall to collidable tiles list
                elif tile_value == 4:
                    # Create an enemy
                    self.enemies.append(Enemy(x, y, tile_width, tile_height, filepath="goblin.png", speed=150))
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "stone_floor.png", 4, 4))
                elif tile_value == 5:
                    # Create a door
                    door = Door(x, y, tile_width, tile_height, filepath="wooden_door.png")
                    self.doors.append(door)
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "stone_floor.png", 4, 4))
                    self.collidable_tiles.append(door)  # Add door to collidable tiles list for collision detection

    # In map.py

    def update(self, delta_time):
        # Update player with collision detection against tiles, doors, and enemies
        self.player.update(delta_time, self.collidable_tiles, self.enemies, self.doors)

        # Update all enemies with collision detection against tiles, doors, and other enemies
        for enemy in self.enemies:
            enemy.update(delta_time, self.collidable_tiles, self.enemies, self.player)

            if enemy.health == 0:
                print("enemy is dead")
                self.enemies.remove(enemy)

        # Handle door updates
        for door in self.doors:
            if door.open:
                self.doors.remove(door)
                self.collidable_tiles.remove(door)

    def draw(self, screen):
        # Get the dimensions of the screen
        screen_width, screen_height = screen.get_size()

        # Calculate the viewport (visible area), centered on the player
        player_x, player_y = self.player.sprite.rect.center
        viewport = pygame.Rect(
            player_x - screen_width // 2,
            player_y - screen_height // 2,
            screen_width,
            screen_height
        )

        # Draw only tiles that are within the viewport
        for tile in self.tiles:
            if viewport.colliderect(tile.sprite.rect):
                tile.draw(screen, self.player.sprite.rect)

        # Draw all doors that are within the viewport
        for door in self.doors:
            if viewport.colliderect(door.sprite.rect):
                door.draw(screen, self.player.sprite.rect)

        # Draw all enemies that are within the viewport
        for enemy in self.enemies:
            if viewport.colliderect(enemy.sprite.rect):
                enemy.draw(screen, self.player.sprite.rect)

        # Draw the player at the center of the screen
        if self.player:
            self.player.draw(screen)
