from creature import Creature
import ability

class Player:
    def __init__(self, mode, **kwargs):
        if (mode == 'init'):
            self.name = kwargs["name"]
            deck = kwargs["deck"]
            self.creatures = []
            self.cards = []
            self.creature_index = 0
            self.finished = "false"
            self.next = ''
            self.discard = 0
            for index in range(0, 5):
                self.cards.append(deck.get_card())
        elif (mode == 'load'):
            json = kwargs["json"]
            self.name = json["name"]
            self.finished = json["finished"]
            self.discard = json["discard"]
            self.next = json["next"]
            self.creature_index = json["creature_index"]
            self.cards = []
            self.creatures = []
            for card in json["cards"]:
                self.cards.append(card)
            for creature in json["creatures"]:
                self.creatures.append(Creature(creature))

    def add_ability(self, creature, card):
        for c in self.cards:
            if (c == card):
                for cr in self.creatures:
                    if (cr.id == creature):
                        if (cr.add_ability(card)):
                            self.cards.remove(card)
                            return True
                        return False
                    return False
        return False

    def add_creature(self, card):
        for c in self.cards:
            if (c == card):
                self.creature_index = self.creature_index + 1
                creature = Creature('init', owner=self.name, card=card, id=self.creature_index)
                self.creatures.append(creature)
                self.cards.remove(card)
                return True
        return False

    def json(self):
        json = {}
        json["name"] = self.name
        json["creatures"] = {}
        json["next"] = self.next
        json["finished"] = self.finished
        json["creature_index"] = self.creature_index
        json["creature"] = []
        for creature in self.creatures:
            json["creatures"].append(creature.json())
        json["cards"] = []
        for card in self.cards:
            json["cards"].append(card)
        json["discard"] = self.discard
        print(json)
        return json
