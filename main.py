import random

import pygame
import sys
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player Stays in the Middle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)
RED = (255, 0, 0)

TILE_SIZE = 50
world_speed = 200  # Speed in pixels per second
GOBLIN_SPEED = 150  # Speed in pixels per second
RANGE = 200  # Range in pixels within which goblins detect the player
GOBLIN_WANDER_INTERVAL = 2  # Interval in seconds for goblins to change direction when wandering


class Sprite:
    def __init__(self, x, y, width, height, image=None, animation_images=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.animation_images = animation_images or []
        self.animation_index = 0
        self.frame_count = 0

    @staticmethod
    def load_image(filepath):
        if os.path.exists(filepath):
            try:
                return pygame.image.load(filepath).convert_alpha()
            except pygame.error as e:
                print(f"Error loading image {filepath}: {e}")
                return None
        else:
            print(f"Image file {filepath} not found.")
            return None

    @staticmethod
    def prepare_tiles(image, rows, cols):
        tiles = []
        if image:
            tile_width = image.get_width() // cols
            tile_height = image.get_height() // rows
            for i in range(rows):
                for j in range(cols):
                    tile_rect = pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height)
                    tiles.append(image.subsurface(tile_rect))
        return tiles

    def draw(self, screen):
        if self.animation_images:
            animation_frame = self.animation_images[self.animation_index]
            screen.blit(animation_frame, self.rect)
        elif self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, RED, self.rect)

    def animate(self, speed=18):
        if self.animation_images:
            self.frame_count += 1
            if self.frame_count >= speed:
                self.frame_count = 0
                self.animation_index = (self.animation_index + 1) % len(self.animation_images)

    def mask(self):
        if self.image:
            return pygame.mask.from_surface(self.image)
        else:
            return None


class Player(Sprite):
    def __init__(self, x, y, width, height, image=None, fireball_images=None):
        super().__init__(x, y, width, height, image)
        self.mana_cost = 25
        self.fireball_images = fireball_images
        self.fireballs = []
        self.world_pos = [x, y]
        self.movement = [0, 0]
        self.health = 100
        self.mana = 100
        self.xp = 100
        self.stamina = 100
        self.direction = ""
        self.last_direction = 'right'

    def handle_input(self, delta_time):
        keys = pygame.key.get_pressed()
        self.movement = [0, 0]
        if keys[pygame.K_LEFT]:
            self.movement[0] = -world_speed * delta_time
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.movement[0] = world_speed * delta_time
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.movement[1] = -world_speed * delta_time
            self.direction = "up"
        if keys[pygame.K_DOWN]:
            self.movement[1] = world_speed * delta_time
            self.direction = "down"
        if keys[pygame.K_q]:
            self.shoot_fireball()

    def decrease_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_dead = True

    def decrease_mana(self, amount):
        self.mana += amount
        if self.mana < 0:
            self.mana = 0

    def increase_xp(self, amount):
        self.xp += amount
        if self.xp >= 100:
            self.xp -= 100

    def shoot_fireball(self):
        if self.mana >= self.mana_cost:
            self.mana -= self.mana_cost
            fireball_rect = pygame.Rect(self.rect.x, self.rect.y, TILE_SIZE // 2, TILE_SIZE // 2)
            self.fireballs.append(Sprite(fireball_rect.x, fireball_rect.y, TILE_SIZE // 2, TILE_SIZE // 2,
                                         animation_images=self.fireball_images))
            self.fireballs[-1].direction = self.last_direction

    def move_fireballs(self, walls, delta_time):
        for fireball in self.fireballs[:]:
            if fireball.direction == 'left':
                fireball.rect.x -= 10 * delta_time
            elif fireball.direction == 'right':
                fireball.rect.x += 10 * delta_time
            elif fireball.direction == 'up':
                fireball.rect.y -= 10 * delta_time
            elif fireball.direction == 'down':
                fireball.rect.y += 10 * delta_time

            # Remove fireball if it goes out of bounds
            if (fireball.rect.x < 0 or fireball.rect.x > WIDTH or
                    fireball.rect.y < 0 or fireball.rect.y > HEIGHT):
                self.fireballs.remove(fireball)
                continue

            # Check for collision with walls
            for wall in walls:
                if fireball.rect.colliderect(wall.rect):
                    self.fireballs.remove(fireball)
                    break

            fireball.animate(speed=18)

    def update_position(self):
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

    def check_collision(self, walls, goblins):
        # Predict the new position
        new_world_pos = [self.world_pos[0] + self.movement[0], self.world_pos[1] + self.movement[1]]
        future_rect = self.rect.copy()
        future_rect.x += self.movement[0]
        future_rect.y += self.movement[1]
        proximity_range = 100
        nearby_walls = [
            wall for wall in walls
            if abs(wall.rect.x - self.world_pos[0]) < proximity_range and
               abs(wall.rect.y - self.world_pos[1]) < proximity_range
        ]
        # Check for collisions with walls
        for wall in nearby_walls:
            wall_rect = wall.rect.move(game.world_offset_x, game.world_offset_y)
            if future_rect.colliderect(wall_rect):
                # Stop movement if a collision is detected
                self.movement = [0, 0]
                break

        # Check for collisions with goblins
        for goblin in goblins:
            if future_rect.colliderect(goblin.rect):
                goblin.attacking = True
                self.movement = [0, 0]  # Stop player movement on collision with goblin
            else:
                goblin.attacking = False

        # Update world position if no collision
        self.world_pos[0] += self.movement[0]
        self.world_pos[1] += self.movement[1]

    def draw_bar(self, screen, current_value, max_value, color, x, y, width, height, label):
        outline_rect = pygame.Rect(x, y, width, height)
        filled_rect = pygame.Rect(x, y, width * (current_value / max_value), height)

        pygame.draw.rect(screen, WHITE, outline_rect, 2)
        pygame.draw.rect(screen, color, filled_rect)

        font = pygame.font.Font(None, 24)
        text = font.render(f"{label}: {current_value}/{max_value}", True, WHITE)
        screen.blit(text, (x + width + 10, y))

    def draw_bars(self, screen):
        self.draw_bar(screen, self.health, 100, RED, 10, HEIGHT - 120, 200, 20, "Health")
        self.draw_bar(screen, self.mana, 100, (0, 100, 255), 10, HEIGHT - 90, 200, 20, "Mana")
        self.draw_bar(screen, self.stamina, 100, (255, 255, 0), 10, HEIGHT - 60, 200, 20, "Stamina")
        self.draw_bar(screen, self.xp, 100, (0, 255, 0), 10, HEIGHT - 30, 200, 20, "XP")


class Goblin(Sprite):
    def __init__(self, x, y, width, height, image=None):
        super().__init__(x, y, width, height, image)
        self.world_pos = [x, y]
        self.movement = [0, 0]
        self.last_direction_change_time = 0
        self.future_rect = self.rect.copy()
        self.attacking = False
        self.damage = 25

        self.attack_cooldown = 2.0  # Cooldown in seconds
        self.last_attack_time = 0  # Track the last attack time

    def update(self, player, walls, delta_time, other_goblins):
        current_time = pygame.time.get_ticks() / 1000.0
        if self.attacking and current_time - self.last_attack_time > self.attack_cooldown:
            player.health -= self.damage
            self.last_attack_time = current_time

        # Movement logic
        distance_x = player.world_pos[0] - self.world_pos[0]
        distance_y = player.world_pos[1] - self.world_pos[1]
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        if distance < RANGE:
            # Move towards the player
            self.movement[0] = GOBLIN_SPEED * delta_time * (distance_x / abs(distance_x)) if abs(distance_x) > 5 else 0
            self.movement[1] = GOBLIN_SPEED * delta_time * (distance_y / abs(distance_y)) if abs(distance_y) > 5 else 0
        elif current_time - self.last_direction_change_time > GOBLIN_WANDER_INTERVAL:
            # Random wandering movement
            self.movement[0] = random.choice([-1, 0, 1]) * GOBLIN_SPEED * delta_time
            self.movement[1] = random.choice([-1, 0, 1]) * GOBLIN_SPEED * delta_time
            self.last_direction_change_time = current_time

        # Stop movement if attacking
        if self.attacking:
            self.movement[0] = 0
            self.movement[1] = 0
        else:
            self.handle_collisions(walls, other_goblins)

        # Update world position after collision handling
        self.world_pos[0] += self.movement[0]
        self.world_pos[1] += self.movement[1]

        # Update goblin rect position relative to the world offset
        self.rect.x = self.world_pos[0] + game.world_offset_x
        self.rect.y = self.world_pos[1] + game.world_offset_y

    def handle_collisions(self, walls, other_goblins):
        self.future_rect = self.rect.copy()
        self.future_rect.x = self.world_pos[0] + self.movement[0]
        self.future_rect.y = self.world_pos[1] + self.movement[1]

        # Check for collisions with walls
        for wall in walls:
            wall_rect = wall.rect
            if self.future_rect.colliderect(wall_rect):
                # Handle collisions in both directions (X and Y)
                self.movement[0] = 0
                self.movement[1] = 0
                return  # Stop checking further if a wall collision is found

        # Check for collisions with other goblins
        for other_goblin in other_goblins:
            if other_goblin != self:
                if self.future_rect.colliderect(other_goblin.future_rect):
                    # Handle collisions in both directions (X and Y)
                    self.movement[0] = 0
                    self.movement[1] = 0
                    return  # Stop checking further if a goblin collision is found


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.x_wall_image = Sprite.load_image('img/stone_walls.png')
        self.y_wall_image = Sprite.load_image('img/stone_walls_side.png')
        self.floor_image = Sprite.load_image('img/stone_floor.png')
        self.player_image = Sprite.load_image('img/wizard.png')
        self.fireball_image = Sprite.load_image('img/fire_ball.png')
        self.smoke_image = Sprite.load_image('img/smoke.png')
        self.blue_potion_image = Sprite.load_image('img/blue_potion.png')
        self.red_potion_image = Sprite.load_image('img/red_potion.png')
        self.goblin_image = Sprite.load_image('img/goblin.png')

        self.x_wall_tiles = Sprite.prepare_tiles(self.x_wall_image, 2, 7)
        self.y_wall_tiles = Sprite.prepare_tiles(self.y_wall_image, 2, 2)
        self.floor_tiles = Sprite.prepare_tiles(self.floor_image, 4, 4)
        self.fireball_images = Sprite.prepare_tiles(self.fireball_image, 1, 3)
        self.floors = []
        self.walls = []
        self.goblins = []
        self.load_level()
        self.player = Player(self.player_start_pos[0], self.player_start_pos[1], TILE_SIZE, TILE_SIZE,
                             self.player_image, self.fireball_images)

    def load_level(self):
        with open('level.json') as f:
            level_data = json.load(f)
        self.player_start_pos = [0, 0]
        for y, row in enumerate(level_data):
            for x, tile in enumerate(row):
                if tile == 0:
                    floor = Sprite(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, random.choice(self.floor_tiles))
                    self.floors.append(floor)
                elif tile == 1:
                    self.player_start_pos = [x * TILE_SIZE, y * TILE_SIZE]
                    floor = Sprite(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, random.choice(self.floor_tiles))
                    self.floors.append(floor)
                elif tile == 2:
                    wall = Sprite(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, random.choice(self.x_wall_tiles))
                    self.walls.append(wall)
                elif tile == 3:
                    wall = Sprite(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, random.choice(self.y_wall_tiles))
                    self.walls.append(wall)
                elif tile == 4:
                    floor = Sprite(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, random.choice(self.floor_tiles))
                    self.floors.append(floor)
                    goblin = Goblin(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, self.goblin_image)
                    self.goblins.append(goblin)

    def run(self):
        while True:
            delta_time = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(delta_time)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, delta_time):
        if self.player.health <= 0:
            self.show_game_over_screen()
            return
        self.player.handle_input(delta_time)
        self.world_offset_x = WIDTH // 2 - self.player.world_pos[0] - self.player.rect.width // 2
        self.world_offset_y = HEIGHT // 2 - self.player.world_pos[1] - self.player.rect.height // 2
        self.player.update_position()
        self.player.check_collision(self.walls, self.goblins)
        for goblin in self.goblins:
            other_goblins = [g for g in self.goblins if g != goblin]
            goblin.update(self.player, self.walls, delta_time, other_goblins)
        for fireball in self.player.fireballs:
            fireball.rect.x += self.world_offset_x
            fireball.rect.y += self.world_offset_y

    def show_game_over_screen(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        screen.fill(BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds
        self.reset_game()

    def reset_game(self):
        self.__init__()  # Reinitialize the game class to reset everything

    def draw(self):
        screen.fill(BLACK)
        for floor in self.floors:
            floor_screen_rect = floor.rect.move(self.world_offset_x, self.world_offset_y)
            screen.blit(floor.image, floor_screen_rect) if floor.image else pygame.draw.rect(screen, BLACK,
                                                                                             floor_screen_rect)

        for wall in self.walls:
            wall_screen_rect = wall.rect.move(self.world_offset_x, self.world_offset_y)
            screen.blit(wall.image, wall_screen_rect) if wall.image else pygame.draw.rect(screen, GREY,
                                                                                          wall_screen_rect)
        for goblin in self.goblins:
            goblin_screen_rect = goblin.rect
            screen.blit(goblin.image, goblin_screen_rect) if goblin.image else pygame.draw.rect(screen, GREEN,
                                                                                                goblin_screen_rect)
        self.player.draw(screen)
        self.player.draw_bars(screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
