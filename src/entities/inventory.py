import json

from src.utilities.file_manager import FileManager


class Inventory:
    def __init__(self, filename):
        self.items = self.load_items(filename)  # Load the item IDs from the JSON file

    def load_items(self, filename):
        return FileManager.load_json_file(filename)["inventory"]

    def add_item(self, item_id):
        # Add item ID (no validation needed since we're only managing IDs here)
        self.items.append(item_id)
        print(f"Added item with ID: {item_id}")

    def remove_item(self, item_id):
        if item_id in self.items:
            self.items.remove(item_id)
            print(f"Removed item with ID: {item_id}")
        else:
            print(f"Error: Item with ID {item_id} not found in inventory.")

    def get_items(self):
        # Return the list of item IDs
        return self.items

    def save_items(self, filename):
        try:
            with open(filename, "w") as file:
                json.dump({"inventory": self.items}, file, indent=4)
            print(f"Inventory saved to '{filename}' successfully.")
        except Exception as e:
            print(f"Error saving inventory to '{filename}': {e}")

    def display_inventory(self):
        # Just print item IDs since we're managing IDs only
        if not self.items:
            print("Inventory is empty.")
        else:
            print("Inventory items by ID:")
            for item_id in self.items:
                print(f"Item ID: {item_id}")

    def equip_item(self, slot, item_id):
        if slot in self.slots:
            self.slots[slot] = item_id
            print(f"Equipped item {item_id} in {slot}.")
        else:
            print(f"Invalid slot {slot} for equipping item {item_id}.")

