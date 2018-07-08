class Creature:
    id = 0
    def __init__(self, owner):
        Creature.id = 1
        self.id = 1
        self.hunger = 1
        self.food = 0
        self.fat = 0
        self.abilities = []
        serf.owner = owner
        print("{} has spawned a new creature (ID: {})".format(self.owner, self.id))
