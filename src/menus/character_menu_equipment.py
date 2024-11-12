import pygame  # Assuming sprite.py is in the same directory or accessible path
from src.entities.sprite import StaticSprite

class CharacterMenuEquipment:
    def __init__(self, item_catalog):
        self.font = pygame.font.Font(None, 36)
        self.item_catalog = item_catalog
        self.sprites = {}  # Store StaticSprite instances for equipped items
        self.player_sprite = None  # Store StaticSprite instance for the player

    def update_equipment(self, player):
        # Update the player's base character image
        if not self.player_sprite:
            self.player_sprite = StaticSprite(0, 0, 100, 100, filepath="adam.png")  # Replace "adam.png" dynamically if needed

        # Retrieve the equipped items from the player
        equipped_items = player.equipped.get_equipped_items()

        # Update equipped items with proper sprites
        for slot, item_id in equipped_items.items():
            if item_id != 0:  # Check if a valid item ID is equipped
                item = self.item_catalog.get_item_by_id(item_id)
                if item:
                    item_src = getattr(item, "src", None)  # Get the image path for the item
                    if item_src:
                        # If the sprite for this slot does not exist, create it
                        if slot not in self.sprites:
                            self.sprites[slot] = StaticSprite(0, 0, 50, 50, filepath=item_src)
                        # If the sprite exists but the image has changed, load the new image
                        elif self.sprites[slot].image is None or self.sprites[slot].image != item_src:
                            self.sprites[slot].load_image(item_src)
            else:
                # If no item is equipped in this slot, remove the sprite if it exists
                if slot in self.sprites:
                    del self.sprites[slot]

    def draw(self, screen, x, y, player):
        # Draw the player's base character image using a StaticSprite
        if self.player_sprite:
            self.player_sprite.rect.topleft = (x, y)
            self.player_sprite.draw(screen)

        # Define specific offsets for each slot; currently set to (0, 0) for centering
        slot_offsets = {
            "head": (0, 0),       # Adjust as needed
            "body": (0, 0),       # Adjust as needed
            "legs": (0, 0),       # Adjust as needed
            "main_hand": (0, 0),  # Adjust as needed
            "off_hand": (0, 0),   # Adjust as needed
        }

        # Display equipped items with proper positioning and overlay
        for slot, sprite in self.sprites.items():
            offset_x, offset_y = slot_offsets.get(slot, (0, 0))
            sprite.rect.topleft = (x + offset_x, y + offset_y)
            sprite.draw(screen)

        # Render the equipment text below or beside the character
        equipped_items = player.equipped.get_equipped_items()
        for i, (slot, item_id) in enumerate(equipped_items.items()):
            item_name = "None" if item_id == 0 else self.item_catalog.get_item_by_id(item_id).name
            equipment_text = self.font.render(f"{slot.capitalize()}: {item_name}", True, (255, 255, 255))
            text_x, text_y = x + 150, y + (30 * i)  # Position text relative to slot order
            screen.blit(equipment_text, (text_x, text_y))
