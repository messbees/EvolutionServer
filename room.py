import json

class Room:
    def __init__(self, name, admin):
        self.name = name
        self.players = []
        self.admin = admin
        self.players.append(admin)
        self.save()

    def connect(self, name):
        for player in self.players:
            if (player == name):
                print("Error! Player with same name is already in this room!")
                return false
        self.players.append(name)
        self.save()
        return true

    def save(self):
        room = {}
        room["players"] = {}
        index = 0
        for player in self.players:
            room["players"][player] = index
            index = index + 1
        room["admin"] = self.admin
        with open('rooms/{}.json'.format(self.name), 'w') as outfile:
            json.dump(room, outfile)
