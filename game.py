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
        self.round = 1
        self.stage = "evolution"
        first = random.choise(players)
        self.turn = first.name

    def json(self):
        json = {}
        json["players"] = {}
        json["deck"] = {}
        json["game"] = {}
        json["game"]["name"] = self.name
        json["game"]["id"] = self.id
        json["game"]["round"] = self.round
        json["game"]["stage"] = self.stage
        json["game"]["turn"] = self.turn
        for player in self.players:
            json["players"][player.name] = player.json()
        return json
