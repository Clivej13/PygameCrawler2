# character_menu.py

import pygame

from src.menus.character_menu_equipment import CharacterMenuEquipment
from src.menus.character_menu_inventory import CharacterMenuInventory
from src.menus.character_menu_quests import CharacterMenuQuests


class CharacterMenu:
    def __init__(self, screen_width, screen_height, item_catalog):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)  # Default font for main text
        self.menu_open = False
        self.selected_tab = "Quests"  # Start with the quests tab selected
        self.tabs = ["Quests", "Inventory", "Equipment"]

        # Create individual tab handlers
        self.character_menu_inventory = CharacterMenuInventory(screen_width, item_catalog)
        self.quests = CharacterMenuQuests()
        self.equipment = CharacterMenuEquipment(item_catalog)

    def update(self, player):
        self.equipment.update_equipment(player)

    def draw(self, screen, player):
        # Draw the background of the character menu
        menu_width, menu_height = self.screen_width * 0.75, self.screen_height * 0.75
        menu_x, menu_y = (self.screen_width - menu_width) // 2, (self.screen_height - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (30, 30, 30), menu_rect)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

        # Draw the main tabs
        tab_width = menu_width / len(self.tabs)
        tab_height = 40
        for i, tab in enumerate(self.tabs):
            tab_x = menu_x + i * tab_width
            tab_y = menu_y
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            if self.selected_tab == tab:
                pygame.draw.rect(screen, (70, 70, 70), tab_rect)  # Highlight selected tab
            pygame.draw.rect(screen, (200, 200, 200), tab_rect, 2)

            # Draw the tab text
            tab_text = self.font.render(tab, True, (255, 255, 255))
            text_x = tab_x + (tab_width - tab_text.get_width()) // 2
            text_y = tab_y + (tab_height - tab_text.get_height()) // 2
            screen.blit(tab_text, (text_x, text_y))

        # Draw the selected tab content
        content_x = menu_x + 20
        content_y = menu_y + tab_height + 20
        if self.selected_tab == "Quests":
            self.quests.draw(screen, content_x, content_y)
        elif self.selected_tab == "Inventory":
            self.character_menu_inventory.draw(screen, content_x, content_y, player)
        elif self.selected_tab == "Equipment":
            self.equipment.draw(screen, content_x, content_y, player)

    def handle_event(self, event, player):
        # Handle character menu specific events for switching tabs and sub-tabs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.switch_tab("left")  # Move to the previous tab with Q
            elif event.key == pygame.K_e:
                self.switch_tab("right")  # Move to the next tab with E
            elif self.selected_tab == "Inventory":  # Handle sub-tab switching for Inventory
                self.character_menu_inventory.handle_event(event, player)

    def switch_tab(self, direction):
        # Switch tabs based on direction: "left" for Q key, "righet" for E key
        current_index = self.tabs.index(self.selected_tab)
        if direction == "left":
            next_index = (current_index - 1) % len(self.tabs)
        elif direction == "right":
            next_index = (current_index + 1) % len(self.tabs)
        else:
            return  # Invalid direction
        self.selected_tab = self.tabs[next_index]

    def toggle_menu(self):
        self.menu_open = not self.menu_open
