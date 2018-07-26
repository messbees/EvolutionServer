class Ability:

    def __init__(self, name, type, action, id):
        self.name = name
        self.type = type
        self.action = action
        self.id = id

    def set_owner(self, owner):
        self.owner = owner

    def apply(self):
        self.action()

cards = {
    "1": Ability("Carnivorous", "This allows you to eat other creatures", "abilty", 1),
    "2": Ability("Fat Tissue", "This allows you to store extra food for next turns", "passive", 2),
    "3": Ability("Running", "This allows you to run away from attacker with 50% chanse", 3),
    "4": Ability("Poisonous", "This kills an attacker after he'll try to kill you", 4)
}

def initialyze():
    abilities = []
    for i in range(1..len(cards)+1):
        for j in range(5):
            abilities.append(cards[str(i)])
    a = []
    for ability in abilities:
        a.append(ability.id)
    return a

def get_ability(id):
    return cards[id]
