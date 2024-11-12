import json

from src.utilities.file_manager import FileManager


class Equipped:
    def __init__(self, filename):
        self.slots = self.load_equipped_items(filename)  # Load equipped items from the JSON file

    def load_equipped_items(self, filename):
        try:
            data = FileManager.load_json_file(filename)
            return data.get("equipped", {"head": 0, "body": 0, "legs": 0})  # Default slots
        except Exception as e:
            print(f"Error loading equipped items: {e}")
            return {"head": 0, "body": 0, "legs": 0}  # Default slots

    def equip_item(self, slot, item_id):
        if slot in self.slots:
            self.slots[slot] = item_id
            print(f"Equipped item with ID {item_id} in slot '{slot}'.")
        else:
            print(f"Error: Slot '{slot}' does not exist.")

    def unequip_item(self, slot):
        if slot in self.slots:
            self.slots[slot] = 0
            print(f"Unequipped item from slot '{slot}'.")
        else:
            print(f"Error: Slot '{slot}' does not exist.")

    def get_equipped_items(self):
        return self.slots

    def save_equipped_items(self, filename):
        try:
            with open(filename, "w") as file:
                json.dump({"equipped": self.slots}, file, indent=4)
            print(f"Equipped items saved to '{filename}' successfully.")
        except Exception as e:
            print(f"Error saving equipped items to '{filename}': {e}")

    def display_equipped_items(self):
        print("Equipped items:")
        items = []
        for item_id in self.slots.items():
            items.append(item_id)
        return items
