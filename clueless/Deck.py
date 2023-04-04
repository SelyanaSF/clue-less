import random

class ClueDeck:
    def __init__(self, players):
        self.players = players
        self.characters = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
        self.rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]
        self.weapons = ["Rope", "Lead Pipe", "Dagger", "Wrench", "Candlestick", "Revolver"]

        # Choose one random character, room, and weapon for the secret deck
        self.secret_deck = [
            self.characters.pop(random.randint(0, len(self.characters)-1)),
            self.rooms.pop(random.randint(0, len(self.rooms)-1)),
            self.weapons.pop(random.randint(0, len(self.weapons)-1))
        ]

        #Add all cards and shuffle
        self.deck = self.characters + self.rooms + self.weapons
        random.shuffle(self.deck)

    # Deal out cards to players 
    def deal(self):
        num_players = len(self.players)
        
        # Create dictionary to hold dealt cards for each player
        dealt_cards = {}
        for i in range(num_players):
            dealt_cards[self.players[i]] = []

        # Deal cards to players
        for i in range(num_players):
            for player in dealt_cards:
                if len(self.deck) == 0:
                    break
                card = self.deck.pop(0)
                dealt_cards[player].append(card)

        # Deal remaining cards in round-robin fashion
        i = 0
        while len(self.deck) > 0:
            player = list(dealt_cards.keys())[i]
            card = self.deck.pop(0)
            dealt_cards[player].append(card)
            i = (i+1) % num_players
        
        # Return a dictionary in the format of player: [dealt cards]
        return dealt_cards

#Note that this class is called in Game.py