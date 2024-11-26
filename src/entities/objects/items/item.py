from src.entities.sprite import StaticSprite


class Item:
    def __init__(self, name, item_type, weight, value, attack_damage=None, armor_rating=None, item_id=None, tier=None, required_skill=None, src=None, equip_slot=None):
        self.id = item_id
        self.name = name
        self.type = item_type
        self.weight = weight
        self.value = value
        self.attack_damage = attack_damage
        self.armor_rating = armor_rating
        self.tier = tier
        self.required_skill = required_skill
        self.src = src  # Source for the item's image
        self.equip_slot = equip_slot
        self.sprite = None  # StaticSprite instance for the item

    def create_sprite(self, x=0, y=0, width=50, height=50):
        """Create a sprite for this item using the provided src if it doesn't already exist."""
        if self.src and self.sprite is None:
            self.sprite = StaticSprite(x, y, width, height, self.src)
            print(f"Sprite created for item '{self.name}' using image '{self.src}'")
        elif self.sprite:
            print(f"Sprite already exists for item '{self.name}'.")

    def update_sprite(self, new_src, x=0, y=0, width=50, height=50):
        """Update the sprite image for the item."""
        self.src = new_src
        if self.sprite is not None:
            self.sprite.load_image(new_src)
            print(f"Sprite updated for item '{self.name}' with new image '{new_src}'")
        else:
            self.create_sprite(x, y, width, height)

    def __str__(self):
        item_details = f"Name: {self.name}, Type: {self.type}, Weight: {self.weight}kg, Value: {self.value} gold, ID: {self.id}"
        if self.attack_damage is not None:
            item_details += f", Attack Damage: {self.attack_damage}"
        if self.armor_rating is not None:
            item_details += f", Armor Rating: {self.armor_rating}"
        if self.tier is not None:
            item_details += f", Tier: {self.tier}"
        if self.required_skill is not None:
            item_details += f", Required {self.required_skill[0]} Skill Level: {self.required_skill[1]}"
        return item_details
