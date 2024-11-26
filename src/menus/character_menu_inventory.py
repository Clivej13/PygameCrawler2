# character_menu_inventory.py

import pygame


class CharacterMenuInventory:
    def __init__(self, screen_width, item_catalog):
        self.screen_width = screen_width
        self.item_catalog = item_catalog  # Reference to the ItemCatalog
        self.sub_menu_font = pygame.font.Font(None, 28)  # Smaller font for sub-tabs
        self.sub_tabs = ["All", "Weapons", "Armor", "Consumable", "Valuables"]
        self.selected_sub_tab = "All"  # Start with "All" items selected
        self.selected_item_index = 0

    def handle_event(self, event, player):
        # Handle user input for inventory interactions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # Navigate down the inventory list
                self.selected_item_index = (self.selected_item_index + 1) % len(player.inventory.get_items())
            elif event.key == pygame.K_w:
                # Navigate up the inventory list
                self.selected_item_index = (self.selected_item_index - 1) % len(player.inventory.get_items())
            elif event.key == pygame.K_RETURN:
                # Equip the selected item
                item_ids = player.inventory.get_items()
                if item_ids:
                    selected_item_id = item_ids[self.selected_item_index]
                    selected_item = self.item_catalog.get_item_by_id(selected_item_id)
                    if selected_item and selected_item.equip_slot:
                        # Equip the item
                        player.equipped.equip_item(selected_item.equip_slot, selected_item_id, player.inventory)
                        player.inventory.remove_item(selected_item_id)
                        player.update_equipped_sprites()

    def switch_sub_tab(self, direction):
        # Switch sub-tabs within Inventory based on direction: "left" for A key, "right" for D key
        current_index = self.sub_tabs.index(self.selected_sub_tab)
        if direction == "left":
            next_index = (current_index - 1) % len(self.sub_tabs)
        elif direction == "right":
            next_index = (current_index + 1) % len(self.sub_tabs)
        else:
            return  # Invalid direction
        self.selected_sub_tab = self.sub_tabs[next_index]
        self.selected_item_index = 0  # Reset item selection when switching sub-tabs

    def draw(self, screen, x, y, player):
        # Draw the sub-tabs for Inventory with a smaller font
        sub_tab_width = (self.screen_width * 0.7) / len(self.sub_tabs)  # Reduce total width and divide among sub-tabs
        sub_tab_height = 30
        for i, sub_tab in enumerate(self.sub_tabs):
            sub_tab_x = x + i * (sub_tab_width + 5)  # Use 5 pixels for spacing between sub-tabs
            sub_tab_y = y
            sub_tab_rect = pygame.Rect(sub_tab_x, sub_tab_y, sub_tab_width, sub_tab_height)
            if self.selected_sub_tab == sub_tab:
                pygame.draw.rect(screen, (70, 70, 70), sub_tab_rect)  # Highlight selected sub-tab
            pygame.draw.rect(screen, (200, 200, 200), sub_tab_rect, 2)

            # Draw the sub-tab text
            sub_tab_text = self.sub_menu_font.render(sub_tab, True, (255, 255, 255))
            text_x = sub_tab_x + (sub_tab_width - sub_tab_text.get_width()) // 2
            text_y = sub_tab_y + (sub_tab_height - sub_tab_text.get_height()) // 2
            screen.blit(sub_tab_text, (text_x, text_y))

        # Update y to draw the items below the sub-tabs
        item_y = y + sub_tab_height + 20

        # Retrieve the list of item IDs from player's inventory
        item_ids = player.inventory.get_items()

        if not item_ids:
            inventory_text = self.sub_menu_font.render("Inventory is empty", True, (255, 255, 255))
            screen.blit(inventory_text, (x, item_y))
        else:
            # Display full item details using the item catalog filtered by sub-tab
            filtered_items = []
            for item_id in item_ids:
                item = self.item_catalog.get_item_by_id(item_id)
                if item:
                    # Filter items based on sub-tab selection
                    if self.selected_sub_tab == "All" or \
                            (self.selected_sub_tab == "Weapons" and item.type in ["One Handed", "Two Handed"]) or \
                            (self.selected_sub_tab == "Armor" and item.type == "Light Armor") or \
                            (self.selected_sub_tab == "Consumable" and item.type == "Consumable") or \
                            (self.selected_sub_tab == "Valuables" and item.type == "Valuable"):
                        filtered_items.append(item)

            if not filtered_items:
                inventory_text = self.sub_menu_font.render(f"No items found for '{self.selected_sub_tab}'", True, (255, 255, 255))
                screen.blit(inventory_text, (x, item_y))
            else:
                for i, item in enumerate(filtered_items):
                    item_text = self.sub_menu_font.render(f"{i + 1}. {item.name} - {item.type} (Value: {item.value} gold)", True, (255, 255, 255))
                    screen.blit(item_text, (x, item_y + i * 30))

            for i, item in enumerate(filtered_items):
                color = (255, 255, 0) if i == self.selected_item_index else (255, 255, 255)
                item_text = self.sub_menu_font.render(f"{i + 1}. {item.name} - {item.type} (Value: {item.value} gold)", True, color)
                screen.blit(item_text, (x, item_y + i * 30))
