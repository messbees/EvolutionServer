class Player:
    def __init__(self, name, deck):
        self.name = name
        self.creatures = []
        self.cards = []
        for index in range(0, 5):
            self.cards.append(deck.get_card())
            
