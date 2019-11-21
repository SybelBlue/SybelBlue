class GameObject:
    _health = 1
    strength = 0
    name = ""

    def __init__(self, name, health):
        self.health = health
        self.name = name

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

        if self._health <= 0:
            self._health = 0
            print("dead")

    def damage(self, dmg):
        self._health -= dmg

    def action_dict(self, other):
        return {"inspect": lambda: print(self.name),
                "hit": lambda: other.damage(self.strength)}


class Player(GameObject):
    potions = 3

    def __init__(self, name):
        super().__init__(name, 10)

    def heal(self):
        self.damage(-3)
        self.potions -= 1

    def action_dict(self, other):
        super_call = super().action_dict(other)
        super_call["heal"] = lambda: self.heal()
        return super_call
