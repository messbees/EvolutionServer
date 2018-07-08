import creature
import player
import deck
import ability
import random

class Game:
    def __init__(self, players):
        self.id = random.randrange(1000, 9999)
        self.deck = Deck()
        self.players = players
