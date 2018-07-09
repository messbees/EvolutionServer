import ability
import random

class Deck:
    def __init__(self):
        self.cards = ability.initialyze()
        print("Created deck with {} cards.".format(self.cards.count))

    def get_card(self):
        card = random.choise(self.cards)
        self.cards.pop(card)
        print("Deck now have {} cards left.".format(self.cards.count))
        return card
