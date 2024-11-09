# player.py

import time
import pygame

from ability import Ability
from sprite import StaticSprite
from status_bars import StatusBars

class Player(StaticSprite):
    def __init__(self, x, y, width, height, filepath=None):
        super().__init__(x, y, width, height, filepath)
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.speed = 150  # Player speed in pixels per second
        self.movement = [0, 0]
        self.health = 50
        self.max_health = 100
        self.damage_taken = []
        self.mana = 80
        self.max_mana = 100
        self.xp = 50
        self.max_xp = 100
        self.stamina = 50
        self.max_stamina = 100
        self.open_door = False
        self.cast_start_time = None
        self.is_casting = False
        self.current_ability = None
        self.portrait_image_path = "img/spellswordportrait.png"

        # Font for displaying damage taken
        self.font = pygame.font.Font(None, 24)  # You can adjust the size as needed
        self.damage_display_time = 1.0  # Display damage for 1 second
        self.target = None  # Add this line to track the selected enemy
        self.abilities = [
            Ability(name="Fireball", damage=40, mana_cost=20, cooldown=3, cast_time=1, melee=False, range=400, icon="img/fireball_icon.png")
        ]  # List of abilities the player can use
        self.enemy_collisions = []
        self.enemy_collision = False

        # Initialize status bars with a reference to the player object itself
        self.status_bars = StatusBars(self)

    def use_ability(self, ability_index, collidable_tiles):
        for enemy in self.enemy_collisions:
            if enemy == self.target:
                self.enemy_collision = True
            else:
                self.enemy_collision = False
        if 0 <= ability_index < len(self.abilities):
            current_time = time.time()

            # Debugging: Starting Ability Usage
            print(f"\nAttempting to use ability at index: {ability_index}")
            print(f"Current time: {current_time}")
            print(f"Player mana: {self.mana}, Target: {self.target}")
            print(f"Is casting: {self.is_casting}")

            if not self.is_casting:
                # Debugging: Looking for abilities to use
                print(f"Not currently casting. Looking for abilities to use...")
                for ability in self.abilities:
                    if self.target is not None:
                        # Debugging: Checking if ability can be used
                        print(f"Checking ability: {ability.name}")
                        if ability.can_use(current_time, self.enemy_collision, self, self.target, collidable_tiles):
                            # Start casting the ability
                            print(f"Starting to cast ability: {ability.name}")
                            self.cast_start_time = current_time
                            self.is_casting = True
                            self.current_ability = ability
                            break
                        else:
                            # Debugging: Ability cannot be used
                            print(f"Ability {ability.name} cannot be used. Cooldown or insufficient mana.")

    def update_casting(self, collidable_tiles):
        for enemy in self.enemy_collisions:
            if enemy == self.target:
                self.enemy_collision = True
            else:
                self.enemy_collision = False
        current_time = time.time()
        if self.is_casting:
            if self.current_ability and (self.cast_start_time + self.current_ability.cast_time <= current_time):
                # Cast ability
                self.current_ability.use(current_time, self)
                self.mana -= self.current_ability.mana_cost
                if self.target:
                    self.target.decrease_health(self.current_ability.damage)
                self.is_casting = False
                self.current_ability = None

    def select_target(self, mouse_pos, enemies):
        # Calculate the offset for the viewport, centered on the player
        screen_width, screen_height = pygame.display.get_surface().get_size()
        offset_x = self.rect.centerx - screen_width // 2
        offset_y = self.rect.centery - screen_height // 2

        # Adjust the mouse position to match the world coordinates
        adjusted_mouse_pos = (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y)

        # Check if the adjusted mouse click is within the bounding box of an enemy
        for enemy in enemies:
            if enemy.rect.collidepoint(adjusted_mouse_pos):
                self.target = enemy  # Set this enemy as the target
                enemy.is_target_of = self
                break
            else:
                self.target = None
        for enemy in enemies:
            if self.target != enemy:
                enemy.is_target_of = None

    def decrease_health(self, amount):
        self.health = max(0, self.health - amount)
        # Record the damage along with the timestamp
        self.damage_taken.append((amount, time.time()))

    def decrease_mana(self, amount):
        self.mana = max(0, self.mana - amount)

    def decrease_stamina(self, amount):
        self.stamina = max(0, self.stamina - amount)

    def handle_input(self, keys):
        # Reset movement to avoid unintended continuous movement
        self.movement = [0, 0]

        # Check key inputs and set movement direction
        if keys[pygame.K_a]:
            self.movement[0] = -1
        if keys[pygame.K_d]:
            self.movement[0] = 1
        if keys[pygame.K_w]:
            self.movement[1] = -1
        if keys[pygame.K_s]:
            self.movement[1] = 1

    def update(self, delta_time, collidable_tiles, enemies, doors):
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        self.handle_input(keys)  # Handle movement input
        self.update_casting(collidable_tiles)

        self.handle_axis_movement(delta_time, 0, collidable_tiles + enemies)  # x-axis
        self.handle_axis_movement(delta_time, 1, collidable_tiles + enemies)  # y-axis

    def handle_axis_movement(self, delta_time, axis, collidable_objects):
        direction = self.movement[axis]
        if direction != 0:
            movement_speed = direction * self.speed * delta_time
            new_rect = self.rect.copy()
            if axis == 0:  # x-axis movement
                new_rect.x += movement_speed
            elif axis == 1:  # y-axis movement
                new_rect.y += movement_speed

            # Collision handling for both axes
            for obj in collidable_objects:
                if new_rect.colliderect(obj.rect):
                    if axis == 0:  # x-axis collision
                        if movement_speed > 0:  # Moving right
                            new_rect.right = obj.rect.left
                        elif movement_speed < 0:  # Moving left
                            new_rect.left = obj.rect.right
                    elif axis == 1:  # y-axis collision
                        if movement_speed > 0:  # Moving down
                            new_rect.bottom = obj.rect.top
                        elif movement_speed < 0:  # Moving up
                            new_rect.top = obj.rect.bottom

            # Update position based on collision detection
            if axis == 0:
                self.rect.x = new_rect.x
            elif axis == 1:
                self.rect.y = new_rect.y

    def draw(self, screen):
        """Draw the player sprite centered on the screen."""
        center_width = screen.get_width() // 2 - self.rect.width // 2
        center_height = screen.get_height() // 2 - self.rect.height // 2
        screen.blit(self.image, (center_width, center_height))
        # Draw the status bars
        self.status_bars.draw(screen)

        # Draw the damage taken above the player's head
        current_time = time.time()
        for damage, timestamp in self.damage_taken[:]:
            # Only show the damage for a limited time
            if current_time - timestamp < self.damage_display_time:
                damage_text = self.font.render(f"-{damage}", True, (255, 0, 0))
                text_x = center_width - damage_text.get_width() // 2
                text_y = center_height - 20  # Positioning above the player's head
                screen.blit(damage_text, (text_x, text_y))
            else:
                # Remove old damage entries
                self.damage_taken.remove((damage, timestamp))

        self.status_bars.draw(screen)
