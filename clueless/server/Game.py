from Tile import * 
from Player import *
from Game_processor import *
from Deck import Deck
from Player import Player

class Game:

    def __init__(self, players, num_players):
        self.num_players = num_players
        self.players = players                              # list of all players
        self.game_deck = Deck.get_deck()                    # dict for initial overall game deck
        self.case_file = Deck.get_secret_deck()             # dict of three secret cards
        # self.turn_state = None                              # turn state for current player
        self.game_status = None                             # game state of entire game

        ############################
        ##### INITIALIZE TILES #####
        # to initialize an object of class tile
        # self, tile_name, tile_type, adjacent_tiles
        ############################
        #
        # INITIALIZE ROOM TILES
        # with their str name, "room", and adj tiles
        tile_study = Tile("Study", "room", ["Hallway 01", "Hallway 03", "Kitchen"])
        tile_hall = Tile("Hall", "room", ["Hallway 01", "Hallway 02"])
        tile_lounge = Tile("Lounge", "room", ["Hallway 02", "Hallway 05", "Conservatory"])
        tile_library = Tile("Library", "room", ["Hallway 03", "Hallway 06", "Hallway 08"])
        tile_billiard_room = Tile("Billiard Room", "room", ["Hallway 06", "Hallway 04", "Hallway 09", "Hallway 07"])
        tile_dining_room = Tile("Dining Room", "room", ["Hallway 05", "Hallway 07", "Hallway 10"])
        tile_conservatory = Tile("Conservatory", "room", ["Hallway 08", "Hallway 11", "Lounge"])
        tile_ballroom = Tile("Ballroom", "room", ["Hallway 11", "Hallway 09", "Hallway 12"])
        tile_kitchen = Tile("Kitchen", "room", ["Hallway 12", "Hallway 10", "Study"])

        # INITIALIZE HALLWAY TILES
        # with their str name, "hallway", and adj tiles
        tile_hallway_01 = Tile("Hallway 01", "hallway", ["Study", "Hall"])
        tile_hallway_02 = Tile("Hallway 02", "hallway", ["Hall", "Lounge"])
        tile_hallway_03 = Tile("Hallway 03", "hallway", ["Study", "Library"])
        tile_hallway_04 = Tile("Hallway 04", "hallway", ["Hall", "Billiard Room"])
        tile_hallway_05 = Tile("Hallway 05", "hallway", ["Lounge", "Dining Room"])
        tile_hallway_06 = Tile("Hallway 06", "hallway", ["Library", "Billiard Room"])
        tile_hallway_07 = Tile("Hallway 07", "hallway", ["Billiard Room", "Dining Room"])
        tile_hallway_08 = Tile("Hallway 08", "hallway", ["Library", "Conservatory"])
        tile_hallway_09 = Tile("Hallway 09", "hallway", ["Billiard Room", "Dining Room"])
        tile_hallway_10 = Tile("Hallway 10", "hallway", ["Dining Room", "Kitchen"])
        tile_hallway_11 = Tile("Hallway 11", "hallway", ["Conservatory", "Ballroom"])
        tile_hallway_12 = Tile("Hallway 12", "hallway", ["Ballroom", "Kitchen"])

        ##### END TILES #####

        ############################
        ##### BOARD DICTIONARY #####
        ############################
        # initialize dictionary of tile_name to tile object
        # referred to as board_dict generally

        self.game_board = {
            # ROOMS
            'Study': tile_study,
            'Hall': tile_hall,
            'Lounge': tile_lounge,
            'Library': tile_library,
            'Billiard Room': tile_billiard_room,
            'Dining Room': tile_dining_room,
            'Conservatory': tile_conservatory,
            'Ballroom': tile_ballroom,
            'Kitchen': tile_kitchen,
            # HALLWAYS
            'Hallway 01' : tile_hallway_01,
            'Hallway 02' : tile_hallway_02,
            'Hallway 03' : tile_hallway_03,
            'Hallway 04' : tile_hallway_04,
            'Hallway 05' : tile_hallway_05,
            'Hallway 06' : tile_hallway_06,
            'Hallway 07' : tile_hallway_07,
            'Hallway 08' : tile_hallway_08,
            'Hallway 09' : tile_hallway_09,
            'Hallway 10' : tile_hallway_10,
            'Hallway 11' : tile_hallway_11,
            'Hallway 12' : tile_hallway_12
            }
        
        # Find out where Game is initialized, loop through players and map their name to id
        # self.player_name_to_connectionid_dict = 

    def get_turn_status(self):
        return self.get_turn_status

    def get_current_player(self):
        return self.get_turn_status

    def get_game_status(self):
        return self.get_turn_status

    def get_case_file(self):
        return self.get_case_file
    
    def get_game_board(self):
        return self.game_board


    # return a player whose turn it is not currently
    def get_player(self, player):
        if player in self.players:
            return self.get_player
        else:
            # unsure what we would want returned here, placeholder print
            print("That player is not in this game, please try again.")

    # A method that deals a deck of cards to players 
    def deal_to_players(self)->dict:
        num_players= len(self.players)
        dealt_decks = Deck.deal(num_players)
        for i, player in enumerate(self.players):
            Player.set_player_hand(dealt_decks[i])


# Khue Test Statements for Move
# show valid moves, prompt, take input is the loop
# test statement

# miss_scarlet = Player("Miss Scarlet", 1)
# players = []
# players.append(miss_scarlet)

# game = Game(players, len(players))

# # movement phase for one player
# while True:
#     show_valid_moves(miss_scarlet, game.get_game_board())
#     move_input = prompt_move(miss_scarlet)
#     move_output = move(game.game_board, miss_scarlet, move_input)

#     if move_output == True:
#         break       # continue to next phase

#     else:
#         print("Invalid move, try again!")

# while True:
#     show_valid_moves(miss_scarlet, game.get_game_board())
#     move_input = prompt_move(miss_scarlet)
#     move_output = move(game.game_board, miss_scarlet, move_input)

#     if move_output == True:
#         break       # continue to next phase

#     else:
#         print("Invalid move, try again!")


