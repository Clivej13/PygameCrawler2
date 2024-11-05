import pygame

class StatusBars:
    def __init__(self, screen_width, screen_height, health, max_health, mana, max_mana, stamina, max_stamina, xp, max_xp):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.health = health
        self.max_health = max_health
        self.mana = mana
        self.max_mana = max_mana
        self.stamina = stamina
        self.max_stamina = max_stamina
        self.xp = xp
        self.max_xp = max_xp

    def update_values(self, health, mana, stamina, xp):
        self.health = health
        self.mana = mana
        self.stamina = stamina
        self.xp = xp

    def draw_bar(self, screen, current_value, max_value, color, shadow_color, x, y, width, height):
        # Ensure the current value does not exceed the maximum
        current_value = max(0, min(current_value, max_value))

        # Draw shadow (background)
        pygame.draw.rect(screen, shadow_color, (x, y, width, height))

        # Draw the filled value bar
        filled_width = (current_value / max_value) * width
        pygame.draw.rect(screen, color, (x, y, filled_width, height))

        # Draw the border around the bar
        outline_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

    def draw(self, screen):
        # Draw the XP bar at the top of the screen with padding
        xp_padding = 20
        xp_height = 25
        xp_y_position = xp_padding

        self.draw_bar(
            screen,
            self.xp, self.max_xp,
            (128, 0, 128), (80, 0, 80),  # Purple color for the XP bar
            xp_padding, xp_y_position,
            self.screen_width - (2 * xp_padding), xp_height
        )

        # Ensure that bars do not overlap and align properly
        # Using constants to properly space them out
        bar_width = 187
        bar_height = 20
        gap_between_bars = 20

        # Calculate the y position such that the bars are properly spaced from each other
        y_position = self.screen_height - 3 * (bar_height + gap_between_bars)

        # Draw health bar
        self.draw_bar(screen, self.health, self.max_health, (255, 0, 0), (128, 0, 0), 10, y_position, bar_width, bar_height)

        # Draw mana bar
        y_position += bar_height + gap_between_bars
        self.draw_bar(screen, self.mana, self.max_mana, (0, 100, 255), (0, 50, 128), 10, y_position, bar_width, bar_height)

        # Draw stamina bar
        y_position += bar_height + gap_between_bars
        self.draw_bar(screen, self.stamina, self.max_stamina, (255, 255, 0), (128, 128, 0), 10, y_position, bar_width, bar_height)
