import pygame

from src.entities.objects.items.item_catalog import ItemCatalog
from src.game.map import Map
from src.menus.character_menu import CharacterMenu

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player Stays in the Middle")


class Game:
    def __init__(self):
        self.delta_time = None
        self.clock = pygame.time.Clock()

        self.item_catalog = ItemCatalog("items.json")
        self.map = Map("level.json", self.item_catalog)

        # Initialize Character Menu
        self.character_menu = CharacterMenu(WIDTH, HEIGHT, self.item_catalog)

    def run(self):
        while True:
            # Calculate delta_time
            self.delta_time = self.clock.tick(60) / 1000.0

            # Handle events, including quit
            self.handle_events()

            # Update the game logic
            self.update()

            # Draw everything
            self.draw()

            # Update the display
            pygame.display.flip()  # Refresh the screen

    def handle_events(self):
        # Event handling, allowing player to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.character_menu.menu_open:
                if event.button == 1:  # Left mouse button is 1
                    # Handle left-click to select target
                    if self.map.player:
                        mouse_pos = pygame.mouse.get_pos()
                        self.map.player.select_target(mouse_pos, self.map.enemies)

            # Handle opening/closing the character menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Toggle character menu
                self.character_menu.update(self.map.player)
                self.character_menu.toggle_menu()

            # Handle character menu specific events if the menu is open
            if self.character_menu.menu_open:
                self.character_menu.handle_event(event, self.map.player)

    def update(self):
        # Update map (player, enemies, and any other entities) only if menu is not open
        if not self.character_menu.menu_open:
            if self.map.player:
                keys = pygame.key.get_pressed()
                self.map.player.handle_input(keys)
                # Ability keys (e.g., 1 for Fireball, 2 for another ability, etc.)
                if keys[pygame.K_1]:
                    self.map.player.use_ability(0, self.map.collidable_tiles)
                elif keys[pygame.K_2]:
                    self.map.player.use_ability(1, self.map.collidable_tiles)

            self.map.update(self.delta_time)

    def draw(self):
        # Clear the screen
        screen.fill((0, 0, 0))  # Fill screen with black

        # Calculate the offset to keep the player centered
        if not self.character_menu.menu_open:
            # Draw map and all entities
            self.map.draw(screen)

        # Draw the character menu if it is open
        if self.character_menu.menu_open:
            self.character_menu.draw(screen, self.map.player)
