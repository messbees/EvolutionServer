import ability

class Creature:
    def __init__(self, mode, **kwargs):
        if (mode == 'init'):
            card = kwargs["card"]
            owner = kwargs["owner"]
            id = kwargs["id"]
            self.id = id
            self.card = card
            self.hunger = 1
            self.food = 0
            self.fat = 0
            self.abilities = []
            self.owner = owner
        if (mode == 'json'):
            json = kwargs["json"]
            self.id == json["id"]
            self.hunger = json["hunger"]
            self.food = json["food"]
            self.fat = json["fat"]
            self.abilities = []
            for ability in json["abilities"]:
                self.abilities.append(ability)
            serf.owner = json["owner"]

    def add_ability(self, card):
        for ability in self.abilities:
            if (card == ability):
                return False
        self.abilities.append(card)
        return True

    def json(self):
        json = {}
        json["id"] = self.id
        json["hunger"] = self.hunger
        json["food"] = self.food
        json["fat"] = self.fat
        json["owner"] = self.owner
        json["abilities"] = {}
        for ability in self.abilities:
            json["abilities"].append(ability)
        json["card"] = card.id
        return json
