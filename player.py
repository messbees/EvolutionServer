import creature
import ability

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.creatures = []
        self.cards = []
        for index in range(0, 5):
            self.cards.append(deck.get_card())

    def json(self):
        json = {}
        json["name"] = self.name
        json["creatures"] = {}
        for creature in self.creatures:
            json["creatures"][creature.id] = creature.json()
        json["cards"] = {}
        for card in self.cards:
            json["cards"].append(card.id)
