import json
import math
import time

import pygame
from wall import Wall
from floor import Floor
from player import Player
from enemy import Enemy
from door import Door


class Map:
    def __init__(self, map_file):
        self.tiles = []
        self.enemies = []
        self.doors = []  # List to store door objects
        self.player = None
        self.collidable_tiles = []  # List to store collidable tiles (walls)

        # Load the map data from a JSON file
        with open(map_file, 'r') as file:
            map_data = json.load(file)

        # Define the size of each tile
        tile_width, tile_height = 50, 50

        # Iterate over the map data and create the appropriate tiles
        for row_idx, row in enumerate(map_data):
            for col_idx, tile_value in enumerate(row):
                x, y = col_idx * tile_width, row_idx * tile_height

                if tile_value == 0:
                    # Create a Floor tile
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "img/stone_floor.png", 4, 4))
                elif tile_value == 1:
                    # Create the waplayer
                    if not self.player:
                        self.player = Player(x, y, tile_width, tile_height, filepath="img/spellsword.png")
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "img/stone_floor.png", 4, 4))
                elif tile_value == 2:
                    wall = Wall(x, y, tile_width, tile_height, "img/stone_walls_x.png", 2, 7)
                    self.tiles.append(wall)
                    self.collidable_tiles.append(wall)  # Add wall to collidable tiles list
                elif tile_value == 3:
                    # Create a wall tile (horizontal or vertical)
                    wall = Wall(x, y, tile_width, tile_height, "img/stone_walls_y.png", 2, 2)
                    self.tiles.append(wall)
                    self.collidable_tiles.append(wall)  # Add wall to collidable tiles list
                elif tile_value == 4:
                    # Create an enemy
                    self.enemies.append(Enemy(x, y, tile_width, tile_height, filepath="img/goblin.png", speed=150))
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "img/stone_floor.png", 4, 4))
                elif tile_value == 5:
                    # Create a door
                    door = Door(x, y, tile_width, tile_height, filepath="img/wooden_door.png")
                    self.doors.append(door)
                    self.tiles.append(Floor(x, y, tile_width, tile_height, "img/stone_floor.png", 4, 4))
                    self.collidable_tiles.append(door)  # Add door to collidable tiles list for collision detection

    # In map.py
    import time
    import math

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
        player_x, player_y = self.player.rect.center
        viewport = pygame.Rect(
            player_x - screen_width // 2,
            player_y - screen_height // 2,
            screen_width,
            screen_height
        )

        # Draw only tiles that are within the viewport
        for tile in self.tiles:
            if viewport.colliderect(tile.rect):
                tile.draw(screen, self.player.rect)

        # Draw all doors that are within the viewport
        for door in self.doors:
            if viewport.colliderect(door.rect):
                door.draw(screen, self.player.rect)

        # Draw all enemies that are within the viewport
        for enemy in self.enemies:
            if viewport.colliderect(enemy.rect):
                enemy.draw(screen, self.player.rect)

        # Draw the player at the center of the screen
        if self.player:
            self.player.draw(screen)
