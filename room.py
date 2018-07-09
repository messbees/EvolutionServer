class Room:
    def __init__(self, name, admin):
        self.name = name
        self.players = []
        self.admin = admin
        self.players.append(admin)
        save()

    def connect(self, name):
        for player in self.players:
            if (player == name):
                print("Error! Player with same name is already in this room!")
                return false
        self.players.append(name)
        save()
        return true

    def save(self):
        room = {}
        room["players"] = {}
        players = room["players"]
        for player in self.players:
            players.append(player)
        room["admin"] = self.admin
        with open('rooms/{}.json'.format(self.name), 'w') as outfile:
            json.dump(room, outfile)
