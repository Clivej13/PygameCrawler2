import math

from sprite import StaticSprite


class Ability:
    def __init__(self, name, damage, mana_cost, cooldown, cast_time=2, melee=True, range=0, icon=None):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost
        self.cooldown = cooldown
        self.cast_time = cast_time
        self.melee = melee
        self.range = range  # 0 for melee, otherwise range in pixels
        self.last_used = - cooldown
        if icon:
            self.icon_sprite = StaticSprite(0, 0, 50, 50, filepath=icon)
        else:
            self.icon_sprite = None

    def can_use(self, current_time, player_collision, enemy, player, collidable_tiles):
        if current_time - self.last_used >= self.cooldown:
            if enemy.mana >= self.mana_cost:
                if self.melee:
                    if player_collision:
                        return True
                elif not self.melee:
                    if self.calculate_distance(enemy, player) < self.range:
                        if not self.is_line_of_sight_blocked(enemy, player, collidable_tiles):
                            return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def calculate_distance(self, enemy, player):
        """Calculate the distance between the enemy and the player."""
        return math.sqrt((player.rect.x - enemy.rect.x) ** 2 + (player.rect.y - enemy.rect.y) ** 2)

    def is_line_of_sight_blocked(self, enemy, player, collidable_tiles):
        """Check if any collidable object is blocking the line of sight to the player."""
        line_start = enemy.rect.center
        line_end = player.rect.center

        for tile in collidable_tiles:
            if tile.rect.clipline(line_start, line_end):
                return True
        return False

    def use(self, current_time, caster):
        """Mark the ability as used."""
        self.last_used = current_time
        caster.last_used = current_time
