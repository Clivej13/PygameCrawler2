# status_bars.py

import time
import pygame

from src.utilities.file_manager import FileManager


class StatusBars:
    def __init__(self, player):
        self.player = player
        self.screen_width = player.screen_width
        self.screen_height = player.screen_height

        # Load portrait image
        self.portrait_image = None
        self.portrait_image = map_data = FileManager.load_image(player.portrait_image_path)

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

    def draw_casting_bar(self, screen):
        if self.player.is_casting and self.player.current_ability:
            current_time = time.time()
            elapsed_time = current_time - self.player.cast_start_time
            cast_duration = self.player.current_ability.cast_time

            if elapsed_time < cast_duration:
                # Draw casting bar
                cast_x = 20
                cast_y = self.screen_height - 140  # Positioned above the action bar
                cast_width = self.screen_width - 40
                cast_height = 20
                fill_width = (elapsed_time / cast_duration) * cast_width

                # Draw background
                pygame.draw.rect(screen, (50, 50, 50), (cast_x, cast_y, cast_width, cast_height))

                # Draw filled bar
                pygame.draw.rect(screen, (0, 255, 0), (cast_x, cast_y, fill_width, cast_height))

                # Draw text for ability name
                font = pygame.font.Font(None, 24)
                text = font.render(f"Casting: {self.player.current_ability.name}", True, (255, 255, 255))
                screen.blit(text, (cast_x + 5, cast_y - 25))

    def draw(self, screen):
        # Draw the XP bar at the top of the screen with padding
        xp_padding = 20
        xp_height = 25
        xp_y_position = xp_padding

        self.draw_bar(
            screen,
            self.player.xp, self.player.max_xp,
            (128, 0, 128), (80, 0, 80),  # Purple color for the XP bar
            xp_padding, xp_y_position,
            self.screen_width - (2 * xp_padding), xp_height
        )

        # Draw the portrait image next to the status bars
        portrait_size = 64
        portrait_x = xp_padding
        portrait_y = xp_y_position + xp_height + 10
        if self.portrait_image:
            screen.blit(self.portrait_image, (portrait_x, portrait_y))

        # Ensure that bars do not overlap and align properly
        bar_width = 187
        bar_height = 20
        gap_between_bars = 10

        # Set the x position for the status bars to align with the right side of the portrait
        bar_x = portrait_x + portrait_size + 10

        # Calculate the y position such that the bars are properly spaced from each other
        y_position = portrait_y

        # Draw health bar
        self.draw_bar(screen, self.player.health, self.player.max_health, (255, 0, 0), (128, 0, 0), bar_x, y_position, bar_width, bar_height)

        # Draw mana bar
        y_position += bar_height + gap_between_bars
        self.draw_bar(screen, self.player.mana, self.player.max_mana, (0, 100, 255), (0, 50, 128), bar_x, y_position, bar_width, bar_height)

        # Draw stamina bar
        y_position += bar_height + gap_between_bars
        self.draw_bar(screen, self.player.stamina, self.player.max_stamina, (255, 255, 0), (128, 128, 0), bar_x, y_position, bar_width, bar_height)

        # Draw the action bar on the screen showing available abilities
        action_bar_x = 20
        action_bar_y = self.screen_height - 70
        icon_size = 50
        padding = 10

        # Draw each ability icon using the StaticSprite class
        for i, ability in enumerate(self.player.abilities):
            if ability.icon_sprite:
                ability.icon_sprite.rect.topleft = (action_bar_x + (icon_size + padding) * i, action_bar_y)
                ability.icon_sprite.draw(screen)

            # Draw cooldown overlay if the ability is on cooldown
            current_time = time.time()
            cooldown_remaining = ability.cooldown - (current_time - ability.last_used)
            if cooldown_remaining > 0:
                cooldown_overlay = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                cooldown_overlay.fill((0, 0, 0, 150))  # Semi-transparent overlay
                screen.blit(
                    cooldown_overlay,
                    (action_bar_x + (icon_size + padding) * i, action_bar_y)
                )

        # Draw the casting bar
        self.draw_casting_bar(screen)
