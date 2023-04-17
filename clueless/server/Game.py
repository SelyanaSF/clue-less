from Deck import Deck
from Player import Player

class Game:

    def __init__(self, num_players, players, game_board, game_deck, case_file, turn_state, game_status):
        self.num_players = num_players
        self.players = players
        self.game_board = game_board
        self.game_deck = Deck.get_deck()
        self.case_file = Deck.get_secret_deck()
        self.turn_state = turn_state
        self.game_status = game_status
        
        # Find out where Game is initialized, loop through players and map their name to id
        # self.player_name_to_connectionid_dict = 

    def get_turn_status():
        pass

    def get_current_player():
        pass

    def get_game_status():
        pass

    def get_case_file():
        pass

    def get_player():
        pass
    
    # A method that deals a deck of cards to players 
    def deal_to_players(self)->dict:
        num_players= len(self.players)
        dealt_decks = Deck.deal(num_players)
        for i, player in enumerate(self.players):
            Player.set_player_hand(dealt_decks[i])
