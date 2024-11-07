import pygame
import random
from sprite import StaticSprite

class Enemy(StaticSprite):
    WANDER, PATROL, CHASE = "WANDER", "PATROL", "CHASE"  # Define states for the enemy

    def __init__(self, x, y, width, height, filepath=None, patrol_points=None, chase_range=150, speed=80):
        super().__init__(x, y, width, height, filepath)
        self.speed = speed  # Enemy speed in pixels per second
        self.state = Enemy.WANDER  # Start with wandering behavior
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]  # Random initial direction
        self.chase_range = chase_range  # Distance at which enemy will start chasing player
        self.health = 50
        self.max_health = 100
        self.mana = 50
        self.max_mana = 100
        self.xp = 50
        self.stamina = 50
        self.max_stamina = 100

        # Optional patrol points for patrolling behavior
        if patrol_points:
            self.patrol_points = patrol_points
            self.patrol_index = 0
            self.state = Enemy.PATROL  # Set state to patrol if patrol points are provided

    def decrease_health(self, amount):
        self.health = max(0, self.health - amount)

    def decrease_mana(self, amount):
        self.mana = max(0, self.mana - amount)

    def decrease_stamina(self, amount):
        self.stamina = max(0, self.stamina - amount)

    def update(self, delta_time, collidable_tiles, enemies, player):
        # Determine the current state based on player proximity
        distance_to_player = ((player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2) ** 0.5
        if distance_to_player <= self.chase_range:
            self.state = Enemy.CHASE
        else:
            self.state = Enemy.PATROL if hasattr(self, 'patrol_points') else Enemy.WANDER

        # Update based on the current state
        if self.state == Enemy.WANDER:
            self.wander(delta_time, collidable_tiles, enemies)
        elif self.state == Enemy.PATROL:
            self.patrol(delta_time, collidable_tiles, enemies)
        elif self.state == Enemy.CHASE:
            self.chase(delta_time, collidable_tiles, enemies, player)

    def wander(self, delta_time, collidable_tiles, enemies):
        # Set the wander speed
        wander_speed = self.speed / 2

        # Randomly change direction occasionally for wandering
        if random.random() < 0.01:  # 1% chance to change direction each frame
            self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

        # Move at half speed for wandering
        self.move(delta_time, collidable_tiles, enemies, None, wander_speed)

    def patrol(self, delta_time, collidable_tiles, enemies):
        # Move towards the current patrol point
        target_x, target_y = self.patrol_points[self.patrol_index]
        direction_vector = [target_x - self.rect.x, target_y - self.rect.y]

        # Normalize the direction
        distance = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5
        if distance != 0:
            self.direction = [direction_vector[0] / distance, direction_vector[1] / distance]

        # Move towards the target patrol point
        self.move(delta_time, collidable_tiles, enemies, None, self.speed)

        # Check if we reached the patrol point
        if abs(target_x - self.rect.x) < 5 and abs(target_y - self.rect.y) < 5:
            # Move to the next patrol point
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)

    def chase(self, delta_time, collidable_tiles, enemies, player):
        # Calculate direction towards the player
        direction_vector = [player.rect.x - self.rect.x, player.rect.y - self.rect.y]

        # Normalize the direction vector
        distance = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5
        if distance != 0:
            self.direction = [direction_vector[0] / distance, direction_vector[1] / distance]

        # Move towards the player at full speed
        self.move(delta_time, collidable_tiles, enemies, player, self.speed)

    def move(self, delta_time, collidable_tiles, enemies, player, speed):
        # Calculate potential movement
        dx = self.direction[0] * speed * delta_time
        dy = self.direction[1] * speed * delta_time

        # Handle x-axis movement and collision
        if dx != 0:
            new_rect = self.rect.copy()
            new_rect.x += dx

            # Check for collisions with collidable tiles, enemies, or the player
            if self.collides(new_rect, collidable_tiles, enemies, player):
                self.direction[0] *= -1  # Reverse direction upon collision
            else:
                # No collision, update x position
                self.rect.x = new_rect.x

        # Handle y-axis movement and collision
        if dy != 0:
            new_rect = self.rect.copy()
            new_rect.y += dy

            # Check for collisions with collidable tiles, enemies, or the player
            if self.collides(new_rect, collidable_tiles, enemies, player):
                self.direction[1] *= -1  # Reverse direction upon collision
            else:
                # No collision, update y position
                self.rect.y = new_rect.y

    def collides(self, new_rect, collidable_tiles, enemies, player):
        # Check collision with collidable tiles
        for tile in collidable_tiles:
            if new_rect.colliderect(tile.rect):
                return True

        # Check collision with other enemies (excluding self)
        for other_enemy in enemies:
            if other_enemy is not self and new_rect.colliderect(other_enemy.rect):
                return True

        # Check collision with the player
        if player and new_rect.colliderect(player.rect):
            return True

        return False

    def draw(self, screen, player_rect):
        """Draw the enemy with an offset based on the player's position."""
        # Calculate the enemy's position with the offset applied for rendering
        offset_x = screen.get_width() // 2 - player_rect.centerx
        offset_y = screen.get_height() // 2 - player_rect.centery

        # Adjust the enemy's position based on the calculated offset
        screen_pos = (self.rect.x + offset_x, self.rect.y + offset_y)
        screen.blit(self.image, screen_pos)
