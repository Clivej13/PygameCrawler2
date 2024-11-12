import json

from src.entities.objects.items.item import Item
from src.utilities.file_manager import FileManager


class ItemCatalog:
    def __init__(self, filename):
        self.items = {}  # Dictionary to store items with their ID as the key
        self.load_items(filename)

    def load_items(self, filename):
        map_data = FileManager.load_json_file(filename)
        for item_data in map_data["items"]:
            item = self.dict_to_item(item_data)
            self.items[item.id] = item  # Use item ID as the key in the dictionary

    def dict_to_item(self, item_dict):
        return Item(
            name=item_dict["name"],
            item_type=item_dict["type"],
            weight=item_dict["weight"],
            value=item_dict["value"],
            attack_damage=item_dict.get("attack_damage"),
            armor_rating=item_dict.get("armor_rating"),
            item_id=item_dict.get("id"),
            tier=item_dict.get("tier"),
            required_skill=tuple(item_dict["required_skill"]) if "required_skill" in item_dict else None,
            src=item_dict.get("src")  # Add image source if available
        )

    def get_item_by_id(self, item_id):
        return self.items.get(item_id, None)

    def get_item_by_name(self, name):
        # Search through the items dictionary and find the first matching name
        for item in self.items.values():
            if item.name == name:
                return item
        return None

    def get_all_items(self):
        return list(self.items.values())

    def create_sprite_for_item(self, item_id, x=0, y=0, width=50, height=50):
        """Create a sprite for the item by its ID."""
        item = self.get_item_by_id(item_id)
        if item:
            item.create_sprite(x, y, width, height)

    def update_item_sprite(self, item_id, new_src, x=0, y=0, width=50, height=50):
        """Update the sprite for a given item by its ID."""
        item = self.get_item_by_id(item_id)
        if item:
            item.update_sprite(new_src, x, y, width, height)
