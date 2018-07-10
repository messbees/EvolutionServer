import ability
import random

class Deck:
    def __init__(self):
        self.cards = ability.initialyze()
        print("Created deck with {} cards.".format(len(self.cards))

    def get_card(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        print("Deck now have {} cards left.".format(len(self.cards))
        return card
