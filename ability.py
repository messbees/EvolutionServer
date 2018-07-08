class Ability:

    def __init__(self, name, type, action, owner):
        self.name = name
        self.type = type
        self.action = action

    def set_owner(self, owner):
        self.owner = owner

    def apply(self):
        self.action()


def initialyze():
    abilities = []
    abilities.append(Ability("Predator", "This allows you to eat other creatures", "abilty"))
    abilities.append(Ability("Fat", "This allows you to store extra food for next turns", "passive"))
    abilities.append(Ability("Predator", "This allows you to eat other creatures", "abilty"))
    abilities.append(Ability("Fat", "This allows you to store extra food for next turns", "passive"))
    abilities.append(Ability("Predator", "This allows you to eat other creatures", "abilty"))
    abilities.append(Ability("Fat", "This allows you to store extra food for next turns", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 1", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 2", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 3", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 4", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 5", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 6", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 7", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 8", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 1", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 2", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 3", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 4", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 5", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 6", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 7", "passive"))
    abilities.append(Ability("Dummy", "This is dummy ability number 8", "passive"))
    return abilities
