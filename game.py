import creature
import player
import deck
import ability
import random

class Game:
    def __init__(self, name, players, deck):
        self.name = name
        self.id = random.randrange(1000, 9999)
        self.round = 1
        self.stage = "evolution"
        first = random.choise(players)
        self.turn = first.name
        self.dice = 0
        self.food = 0
        self.players = players
        self.deck = deck

    def do_evolution(self, player, creature, card):
        if (creature = 999):
            self.players[player].add_creature(card)
        else:
            for c in self.players[player].creatures:
                if (c.id == creature):
                    c.add_ability(card)
                    print('Creature {} of {} now have ability"{}".'.format(c.id, player.name, card))

    def json(self):
        json = {}
        json["game"] = {}
        json["game"]["name"] = self.name
        json["game"]["id"] = self.id
        json["game"]["round"] = self.round
        json["game"]["stage"] = self.stage
        json["game"]["turn"] = self.turn
        json["game"]["dice"] = self.dice
        json["game"]["food"] = self.food
        json["players"] = {}
        for player in self.players:
            json["players"][player.name] = player.json()
        json["deck"] = {}
        for card in self.deck:
            json["deck"].append(card.id)
        return json
