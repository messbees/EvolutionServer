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
        first = random.choice(players)
        self.turn = first.name
        self.players = players
        for index in (0, len(self.players)-2):
            players[index].next = players[index+1]
        players[len(self.players)-1].next = first
        self.dice = 0
        self.food = 0
        self.deck = deck
        self.save()
        print("Game {} created.".format(self.id))

    def do_evolution(self, player, creature, card):
        if not (self.turn == player.name):
            return false

        for p in self.players:
            if (p == player):
                player = p
        else:
            return false

        if (creature == 999):
            player.add_creature(card)

        else:
            cc = None
            for c in player.creatures:
                if (c.id == creature):
                    c.add_ability(card)
                    cc = c
                    print('Creature {} of {} now have ability"{}" from {}.'.format(c.id, player.name, card, player.name))
            if (cc == None):
                return false

        if (creature == 0 and player.finished == "false"):
            player.finished = "true"


        for p in self.players:
            if (p.finished == "false"):
                return true

        self.stage = "survival"
        self.turn = first.name

    def save(self):
        game = self.json()
        with open('games/{}.json'.format(self.id), 'w') as outfile:
            json.dump(game, outfile)

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
