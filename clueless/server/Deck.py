import random

class Deck:
    def __init__(self):
        # self.num_players = num_players
        self.characters = {"Miss Scarlet": "character", "Colonel Mustard": "character", "Mrs. White": "character", "Mr. Green": "character", "Mrs. Peacock": "character", "Professor Plum": "character"}
        self.rooms = {"Kitchen": "room", "Ballroom": "room", "Conservatory": "room", "Dining Room": "room", "Billiard Room": "room", "Library": "room", "Lounge": "room", "Hall": "room", "Study": "room"}
        self.weapons = {"Rope": "weapon", "Lead Pipe": "weapon", "Dagger": "weapon", "Wrench": "weapon", "Candlestick": "weapon", "Revolver": "weapon"}

        # Choose one random character, room, and weapon for the secret deck
        self.secret_deck = {
            random.choice(list(self.characters.keys())): "character",
            random.choice(list(self.rooms.keys())): "room",
            random.choice(list(self.weapons.keys())): "weapon"
        }

        # Create the deck as a dictionary with key-value pairs {card value: card type}
        self.deck = {}
        for card_type in [self.characters, self.rooms, self.weapons]:
            for card_name in card_type.keys():
                if card_name not in self.secret_deck.keys():
                    self.deck[card_name] = card_type[card_name]
        
        # Shuffle the deck of cards
        shuffled_keys = list(self.deck.keys())
        random.shuffle(shuffled_keys)
        self.deck = {key: self.deck[key] for key in shuffled_keys}

    def __repr__(self):
        # Return a string representation of the dictionaries
        return f"Game_deck: {self.deck}"
    
    def get_deck(self):
        return self.deck
    
    def get_secret_deck(self):
        return self.secret_deck
    
    # A method that creates player decks based on the number of players
    def deal(self, num_players)->list:
        game_deck= self.get_deck()

        dealt_decks = [{} for i in range(num_players)]

        num_dicts= len(dealt_decks)
        game_deck_keys= list(game_deck.keys())
        for i, key in enumerate(game_deck_keys):
            dealt_deck= dealt_decks[i % num_dicts]
            dealt_deck[key]= game_deck[key]
        return dealt_decks # returns a list of decks in the form of dictionaries
     


    # A method that deals a deck of cards to players 
    # players passed into deck should be a list
    # Assigned the method to game as deal_to_players()

    # def deal_to_players(self,players)->dict:
    #     num_players= len(players)
    #     dealt_decks= self.deal(num_players)
    #     player_w_cards = {key: value for key, value in zip(players, dealt_decks)}
    #     return player_w_cards
   

# Driver code
# This should can be called in the game class
# deck= Deck()
# players= ["katie","megan", "kweku", "sely", "khue"]
# print(deck.get_secret_deck())
# print()
# print(deck.get_deck())
# print()
# print(deck.deal(players))
# print()