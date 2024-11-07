import pygame
from map import Map

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player Stays in the Middle")


class Game:
    def __init__(self):
        self.delta_time = None
        self.clock = pygame.time.Clock()

        # Load the map, including player, enemies, and all tiles
        self.map = Map("level.json")  # Load the map from JSON file

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right mouse button is 3
                    pass
                if event.button == 1:  # Left mouse button is 1
                    pass

        # Handle player input
        keys = pygame.key.get_pressed()
        if self.map.player:
            self.map.player.handle_input(keys)

    def update(self):
        # Update map (player, enemies, and any other entities)
        self.map.update(self.delta_time)

    def draw(self):
        # Clear the screen
        screen.fill((0, 0, 0))  # Fill screen with black

        # Calculate the offset to keep the player centered
        if self.map.player:
            # Draw map and all entities
            self.map.draw(screen)


if __name__ == "__main__":
    game = Game()
    game.run()
