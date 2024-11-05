import pygame
from sprite import StaticSprite
from status_bars import StatusBars  # Assuming StatusBars is saved in status_bars.py
from attack_direction_indicator import \
    AttackDirectionIndicator  # Assuming the new class is saved in attack_direction_indicator.py


class Player(StaticSprite):
    def __init__(self, x, y, width, height, filepath=None):
        super().__init__(x, y, width, height, filepath)
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.speed = 150  # Player speed in pixels per second
        self.movement = [0, 0]
        self.health = 50
        self.max_health = 100
        self.mana = 50
        self.max_mana = 100
        self.xp = 50
        self.max_xp = 100
        self.stamina = 50
        self.max_stamina = 100
        self.open_door = False

        # Create an instance of StatusBars
        self.status_bars = StatusBars(
            self.screen_width, self.screen_height,
            self.health, self.max_health,
            self.mana, self.max_mana,
            self.stamina, self.max_stamina,
            self.xp, self.max_xp
        )

        # Create an instance of AttackDirectionIndicator
        self.attack_indicator = AttackDirectionIndicator(self.screen_width, self.screen_height)

    def decrease_health(self, amount):
        self.health = max(0, self.health - amount)

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

        self.handle_axis_movement(delta_time, 0, collidable_tiles + enemies)  # x-axis
        self.handle_axis_movement(delta_time, 1, collidable_tiles + enemies)  # y-axis

        # Update the status bar values
        self.status_bars.update_values(self.health, self.mana, self.stamina, self.xp)

        # Update the attack direction indicator
        self.attack_indicator.update()

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

    def interact_with_doors(self, doors):
        print("Attempt to open door")

        # Calculate the same offsets applied when rendering the doors
        offset_x = self.screen_width // 2 - self.rect.centerx
        offset_y = self.screen_height // 2 - self.rect.centery

        # Adjust the attack indicator rect by the offset
        adjusted_attack_indicator_rect = self.attack_indicator.rect.move(-offset_x, -offset_y)

        for door in doors:
            if adjusted_attack_indicator_rect.colliderect(door.rect):
                print("Collide with door")
                door.open = True

    def draw(self, screen):
        """Draw the player sprite centered on the screen."""
        screen.blit(self.image, (screen.get_width() // 2 - self.rect.width // 2,
                                 screen.get_height() // 2 - self.rect.height // 2))
        # Draw the status bars
        self.status_bars.draw(screen)

        # Draw the attack direction indicator
        self.attack_indicator.draw(screen)
