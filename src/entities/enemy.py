import time

import pygame
import random

from src.entities.abilities.ability import Ability
from src.entities.sprite import StaticSprite


class Enemy:
    WANDER, PATROL, CHASE, STAND = "WANDER", "PATROL", "CHASE", "STAND"  # Define states for the enemy

    def __init__(self, x, y, width, height, filepath=None, patrol_points=None, chase_range=300, speed=80):
        # Use StaticSprite as a composition
        self.sprite = StaticSprite(x, y, width, height, filepath)
        self.player_collision = False
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
        self.is_casting = False
        self.cast_start_time = None
        self.last_used = 0
        self.is_target_of = None

        # Optional patrol points for patrolling behavior
        if patrol_points:
            self.patrol_points = patrol_points
            self.patrol_index = 0
            self.state = Enemy.PATROL  # Set state to patrol if patrol points are provided
        self.abilities = [
            Ability("Claw Swipe", damage=10, mana_cost=5, cooldown=5, melee=True),
            Ability("Dark Bolt", damage=30, mana_cost=5, cooldown=3, cast_time=5, melee=False, range=300)
        ]
        self.target = None

    def decrease_health(self, amount):
        self.health = max(0, self.health - amount)

    def decrease_mana(self, amount):
        self.mana = max(0, self.mana - amount)

    def decrease_stamina(self, amount):
        self.stamina = max(0, self.stamina - amount)

    def use_ability(self, player, collidable_tiles):
        current_time = time.time()
        if self.is_casting:
            if self.current_ability.can_use(current_time, self.player_collision, self, player, collidable_tiles):
                if self.cast_start_time + self.current_ability.cast_time <= current_time:
                    self.current_ability.use(current_time, self)
                    self.mana -= self.current_ability.mana_cost
                    player.decrease_health(self.current_ability.damage)
                    self.is_casting = False
            else:
                self.is_casting = False
        else:
            for ability in self.abilities:
                if self.target is not None:
                    if ability.can_use(current_time, self.player_collision, self, player, collidable_tiles):
                        self.cast_start_time = current_time
                        self.is_casting = True
                        self.current_ability = ability

    def update(self, delta_time, collidable_tiles, enemies, player):
        # Determine the current state based on player proximity
        distance_to_player = ((player.sprite.rect.x - self.sprite.rect.x) ** 2 + (player.sprite.rect.y - self.sprite.rect.y) ** 2) ** 0.5
        if distance_to_player <= self.chase_range:
            self.state = Enemy.CHASE
        else:
            self.state = Enemy.PATROL if hasattr(self, 'patrol_points') else Enemy.WANDER

        # Update based on the current state
        if self.state == Enemy.WANDER:
            self.wander(delta_time, collidable_tiles, enemies)
            self.target = None
        elif self.state == Enemy.PATROL:
            self.patrol(delta_time, collidable_tiles, enemies)
            self.target = None
        elif self.state == Enemy.CHASE:
            self.chase(delta_time, collidable_tiles, enemies, player)
            self.target = player
        self.use_ability(player, collidable_tiles)

    def draw_casting_bar(self, screen, offset_x, offset_y):
        """Draw the casting progress bar below the enemy."""
        if self.is_casting:
            # Calculate casting progress
            current_time = time.time()
            elapsed_time = current_time - self.cast_start_time
            cast_progress = min(1.0, elapsed_time / self.current_ability.cast_time)

            # Define bar dimensions
            bar_width = self.sprite.rect.width
            bar_height = 5
            bar_x = self.sprite.rect.x + offset_x
            bar_y = self.sprite.rect.y + self.sprite.rect.height + offset_y + 5  # Position below the enemy

            # Draw background bar (in gray)
            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

            # Draw progress bar (in green)
            progress_width = bar_width * cast_progress
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, progress_width, bar_height))

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
        direction_vector = [target_x - self.sprite.rect.x, target_y - self.sprite.rect.y]

        # Normalize the direction
        distance = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5
        if distance != 0:
            self.direction = [direction_vector[0] / distance, direction_vector[1] / distance]

        # Move towards the target patrol point
        self.move(delta_time, collidable_tiles, enemies, None, self.speed)

        # Check if we reached the patrol point
        if abs(target_x - self.sprite.rect.x) < 5 and abs(target_y - self.sprite.rect.y) < 5:
            # Move to the next patrol point
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)

    def chase(self, delta_time, collidable_tiles, enemies, player):
        # Calculate direction towards the player
        direction_vector = [player.sprite.rect.x - self.sprite.rect.x, player.sprite.rect.y - self.sprite.rect.y]

        # Normalize the direction vector
        distance = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5
        if distance != 0:
            self.direction = [direction_vector[0] / distance, direction_vector[1] / distance]

        # Move towards the player at full speed
        self.move(delta_time, collidable_tiles, enemies, player, self.speed)

    def move(self, delta_time, collidable_tiles, enemies, player, speed):
        if not self.is_casting:
            # Calculate potential movement
            dx = self.direction[0] * speed * delta_time
            dy = self.direction[1] * speed * delta_time

            # Handle x-axis movement and collision
            if dx != 0:
                new_rect = self.sprite.rect.copy()
                new_rect.x += dx

                # Check for collisions with collidable tiles, enemies, or the player
                if self.collides(new_rect, collidable_tiles, enemies, player):
                    self.direction[0] *= -1  # Reverse direction upon collision
                else:
                    # No collision, update x position
                    self.sprite.rect.x = new_rect.x

            # Handle y-axis movement and collision
            if dy != 0:
                new_rect = self.sprite.rect.copy()
                new_rect.y += dy

                # Check for collisions with collidable tiles, enemies, or the player
                if self.collides(new_rect, collidable_tiles, enemies, player):
                    self.direction[1] *= -1  # Reverse direction upon collision
                else:
                    # No collision, update y position
                    self.sprite.rect.y = new_rect.y

    def collides(self, new_rect, collidable_tiles, enemies, player):
        if player and new_rect.colliderect(player.sprite.rect):
            self.player_collision = True
            player.enemy_collisions.append(self)
            return True
        else:
            self.player_collision = False
            if player is not None:
                if self in player.enemy_collisions:
                    player.enemy_collisions.remove(self)
        for tile in collidable_tiles:
            if new_rect.colliderect(tile.sprite.rect):
                return True
        for other_enemy in enemies:
            if other_enemy is not self and new_rect.colliderect(other_enemy.sprite.rect):
                return True
        return False

    def draw(self, screen, player_rect):
        """Draw the enemy with an offset based on the player's position."""
        # Calculate the enemy's position with the offset applied for rendering
        offset_x = screen.get_width() // 2 - player_rect.centerx
        offset_y = screen.get_height() // 2 - player_rect.centery

        # Adjust the enemy's position based on the calculated offset
        screen_pos = (self.sprite.rect.x + offset_x, self.sprite.rect.y + offset_y)
        screen.blit(self.sprite.image, screen_pos)

        # Draw the casting bar if the enemy is casting
        self.draw_casting_bar(screen, offset_x, offset_y)

        # If this enemy is selected, draw a highlight
        if self.is_target_of is not None:
            pygame.draw.rect(screen, (255, 0, 0), self.sprite.rect.move(offset_x, offset_y), 2)
