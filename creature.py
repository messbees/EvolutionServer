import player
import ability

class Creature:
    id = 0
    def __init__(self, owner, card):
        Creature.id = 1
        self.card = card
        self.id = 1
        self.hunger = 1
        self.food = 0
        self.fat = 0
        self.abilities = []
        serf.owner = owner
        print("{} has spawned a new creature (ID: {})".format(self.owner, self.id))

    def json(self):
        json = {}
        json["id"] = self.id
        json["hunger"] = self.hunger
        json["food"] = self.food
        json["fat"] = self.fat
        json["owner"] = self.owner
        json["abilities"] = {}
        for ability in self.abilities:
            json["abilities"] = ability.id
        json["card"] = card.id
