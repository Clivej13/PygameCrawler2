import json
from ability import Ability  # Assuming Ability class is imported from the ability module


class AbilityCatalog:
    def __init__(self, filename=None):
        self.abilities = {}  # Dictionary to store abilities with their name as the key
        if filename:
            self.load_abilities(filename)

    def load_abilities(self, filename):
        """Load abilities from a JSON file."""
        with open(filename, "r") as file:
            data = json.load(file)
            for ability_data in data.get("abilities", []):
                ability = self.dict_to_ability(ability_data)
                self.abilities[ability.name] = ability

    def dict_to_ability(self, ability_dict):
        """Convert a dictionary to an Ability object."""
        return Ability(
            name=ability_dict["name"],
            damage=ability_dict["damage"],
            mana_cost=ability_dict["mana_cost"],
            cooldown=ability_dict["cooldown"],
            cast_time=ability_dict.get("cast_time", 2),
            melee=ability_dict.get("melee", True),
            range=ability_dict.get("range", 0),
            icon=ability_dict.get("icon")
        )

    def get_ability_by_name(self, name):
        """Retrieve an ability by its name."""
        return self.abilities.get(name, None)

    def get_all_abilities(self):
        """Get a list of all abilities."""
        return list(self.abilities.values())