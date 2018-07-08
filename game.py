import creature
import player
import deck
import ability
import random

class Game:
    def __init__(self, name, players, deck):
        self.name = name
        self.id = random.randrange(1000, 9999)
        self.deck = deck
        self.players = players
