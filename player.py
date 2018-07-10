import creature
import ability

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.creatures = []
        self.cards = []
        self.finished = "true"
        self.discard = 0
        for index in range(0, 5):
            self.cards.append(deck.get_card())

    def add_creature(self, card):
        creature = Creature(self, card)
        self.creatures.append(creature)

    def json(self):
        json = {}
        json["name"] = self.name
        json["creatures"] = {}
        json["finished"] = self.finished
        for creature in self.creatures:
            json["creatures"][creature.id] = creature.json()
        json["cards"] = []
        for card in self.cards:
            json["cards"].append(card.id)
        json["discard"] = self.discard
        return json
