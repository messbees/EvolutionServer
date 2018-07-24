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


def initialyze():
    abilities = []
    abilities.append(Ability("Predator", "This allows you to eat other creatures", "abilty", 1))
    abilities.append(Ability("Fat", "This allows you to store extra food for next turns", "passive", 2))
    abilities.append(Ability("Predator", "This allows you to eat other creatures", "abilty", 1))
    abilities.append(Ability("Fat", "This allows you to store extra food for next turns", "passive", 2))
    abilities.append(Ability("Predator", "This allows you to eat other creatures", "abilty", 1))
    abilities.append(Ability("Fat", "This allows you to store extra food for next turns", "passive", 2))
    abilities.append(Ability("Dummy", "This is dummy ability number 1", "passive", 3))
    abilities.append(Ability("Dummy", "This is dummy ability number 2", "passive", 4))
    abilities.append(Ability("Dummy", "This is dummy ability number 3", "passive", 5))
    abilities.append(Ability("Dummy", "This is dummy ability number 4", "passive", 6))
    abilities.append(Ability("Dummy", "This is dummy ability number 5", "passive", 7))
    abilities.append(Ability("Dummy", "This is dummy ability number 6", "passive", 8))
    abilities.append(Ability("Dummy", "This is dummy ability number 7", "passive", 9))
    abilities.append(Ability("Dummy", "This is dummy ability number 8", "passive", 10))
    abilities.append(Ability("Dummy", "This is dummy ability number 1", "passive", 3))
    abilities.append(Ability("Dummy", "This is dummy ability number 2", "passive", 4))
    abilities.append(Ability("Dummy", "This is dummy ability number 3", "passive", 5))
    abilities.append(Ability("Dummy", "This is dummy ability number 4", "passive", 6))
    abilities.append(Ability("Dummy", "This is dummy ability number 5", "passive", 7))
    abilities.append(Ability("Dummy", "This is dummy ability number 6", "passive", 8))
    abilities.append(Ability("Dummy", "This is dummy ability number 7", "passive", 9))
    abilities.append(Ability("Dummy", "This is dummy ability number 8", "passive", 10))
    a = []
    for ability in abilities:
        a.append(ability.id)
    return a
