import json

class Room:
    def __init__(self, name, admin):
        self.name = name
        self.players = []
        self.admin = admin
        self.save()
        print('Opening room named {} by {}'.format(name, admin))

    def connect(self, name):
        print("{} is in room {}".format(name, self.name))
        for player in self.players:
            if (player == name):
                print("Error! Player with same name is already in this room!")
                return False
        self.players.append(name)
        self.save()
        return True

    def save(self):
        room = {}
        room["players"] = []
        room["name"] = self.name
        room["status"] = 'waiting'
        for player in self.players:
            room["players"].append(player)
        room["admin"] = self.admin
        with open('rooms/{}.json'.format(self.name), 'w') as outfile:
            json.dump(room, outfile)
