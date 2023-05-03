import random
from clueless.server.Player import Player
from clueless.server.Tile import Tile

class Game_processor:
    # WEAPONS = ['candlestick','dagger','leadpipe','revolver','rope','wrench']
    # TOKENS = ['Professor Plum','Mrs Peacock','Mr Green','Mrs White','Miss Scarlet','Colonel Mustard']
    # ROOMS = ['Study','Library','Lounge', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen']

    # def __init__(self, players, weapons, rooms, solution):
    #     self.players = players
    #     self.weapons = weapons
    #     self.rooms = rooms
    #     self.solution = solution
    #     self.cards = players + weapons + rooms
    #     self.deck = self.cards.copy()
    #     random.shuffle(self.deck)
    #     self.player_positions = {player: None for player in players}
    #     self.suggestions = []
    #     self.accusations = []
    #     self.player_cards = {player: [] for player in players}
    #     self.game_over = False

    # def __init__(self) -> None:
    #     pass


#      # This method deals out the cards in the deck to each player. It does not
#      # return anything, but it modifies the player_cards and deck attributes 
#      # of the ClueGame object.   
#     def deal_cards(self):
#         for i, card in enumerate(self.deck):
#             self.player_cards[self.players[i % len(self.players)]].append(card)
#         self.deck = []

    


    def get_valid_moves(board_dict, player):

        valid_tile_names = []

        # define strings for first move tiles
        if player.get_player_old_location() is None and player.get_player_current_location() is None:
            player_first_move = {
                'Miss Scarlet' : 'Hallway 02',
                'Professor Plum' : 'Hallway 03',
                'Colonel Mustard' : 'Hallway 05',
                'Mrs. Peacock' : 'Hallway 08',
                'Mr. Green' : 'Hallway 11',
                'Mrs. White' : 'Hallway 12'
                }
            
            valid_tile_names.append(player_first_move.get(player.get_player_name()))
        
        else:
            
            # get adjacent tiles for that tile
            temp_adjacent_tiles = board_dict.get(player.get_player_current_location()).get_adjacent_tiles()

            valid_tile_names.append(player.get_player_current_location().get_tile_name())

            # check if the player is allowed to move there
            for tile in temp_adjacent_tiles:
            # if NO ONE is on the tile, then automatically valid move (adj and empty); append to valid tiles
            #   else if the tile type is ROOM and there are 1 or more players on it, this is also valid, append
            # all other cases are INVALID (1 player and HALLWAY is invalid, hallway is considered full)

                if board_dict.get(tile).get_tile_num_players() == 0:
                    valid_tile_names.append(tile.get_tile_name())

                elif board_dict.get(tile).get_tile_num_players() >= 1 and board_dict.get(tile).get_tile_type() == "room":
                    valid_tile_names.append(tile.get_tile_name())
        
        # may need to convert to frontend names
        return valid_tile_names

    def move(board_dict, player, destination):
        # get backend tile name

        old_location_obj = player.get_player_old_location()
        old_location_name = ''
        
        player.update(destination)
        # Get current location AFTER updating the player's location
        curr_location_obj = player.get_player_current_location()
        curr_location_name = curr_location_obj.get_tile_name()
        # Incremement the now occupied tile by 1
        board_dict.get(curr_location_name).tile_num_players += 1
        
        # Decrement the old tile by 1 if it exists (not None)
        if old_location_obj is not None:
            old_location_name = old_location_obj.get_tile_name()
            board_dict.get(old_location_name).tile_num_players -= 1



    # # This method determines what turn the player is taking and then routes to 
    # # appropriate game logic functions to carry out turn accordingly
    # def player_take_turn(player_turn):
    #     print("Player taking turn: Player ", player_turn['player_id'])

    #     if player_turn['turn_status'] == "movement":
    #         print("Player chooses to move to location ", player_turn['target_tile'])
    #         print()

        # if player_turn['turn_status'] == "movement":
        #     print("Player chooses to move to location ", player_turn['target_tile'])
        #     print()

    #   return player_turn
    #     return player_turn

    # This method records an accusation made by a player. It does not return
    # anything, but it modifies the accusations attribute of the ClueGame object. 
    # If the accusation is correct
    def accuse(player, weapon, room, case_file):
        case_file_reversed = {card_type: card_val for card_val, card_type in case_file.items()}
        # If accusation is correct, return True
        return player == case_file_reversed['character'] and weapon == case_file_reversed['weapon'] and room == case_file_reversed['room']   

        
    def suggest(suggest_dict, players, board_dict):
        # NEEDS TO MOVE PLAYER TO PLAYER'S ROOM
        # suggested_room = board_dict.suggestplayer.get_player_current_location()

        # move the suggested player first
        # find the player in the list with the value of 'player' entry in suggest_cards
        for suggested_player in players:
            if suggested_player.player_name == suggest_dict.get('character'):
                # update the location
                # DEFINE WHAT OLD LOCATION MEANS
                # if old location means anything before your own turn
                # then old_location and current_location should be equal
                # we may need new setter functions in player
                # OR, we use if_placed flag for player

                # check the player's current location against the entry in the suggest_dict
                # update the suggested player's location
                if suggested_player.get_player_current_location().get_tile_name() != suggest_dict.get('room'):
                    placed_tile = board_dict.get(suggest_dict.get('room'))
                    suggested_player.update(placed_tile)
                    print(suggested_player.player_name, "has been moved to", suggested_player.get_player_current_location().get_tile_name(), "!")
                    # suggested_player.if_placed = False
                else:
                    print()
                    print("error checking")
                    # suggested_player.if_placed = True
                    

                # change numbers of players on each tile, old and new
                if suggested_player.get_player_old_location() is not None:
                    # print("Flag", suggested_player.get_player_old_location().get_tile_name())
                    suggested_player.get_player_old_location().tile_num_players -= 1

                suggested_player.get_player_current_location().tile_num_players += 1
                
                # return if_placed flag for player?
                break 

            else:
                continue
                # print(suggested_player.get_player_name(), "is not the player with that name.")

    def get_suggest_matches_for_player(player, suggest_dict, players):
        # looping through all players in Game.players EXCEPT for current player
        # if any entry in dictionary matches 
        # print()
        # print("Can you disprove this suggestion? Show", player.get_player_name(), "a matching card if you do!")
        # print()

        match_found = False
        other_player = "No player has a matching card!"
        matched_card = "No matched card found!"

        print("player")

        for other_player in players:
            if other_player != player:
                # print("    Checking", other_player.get_player_name(), "for matching cards...")
                # print()
                
                print("other_player is", other_player.get_player_name())
                print("suggest_dict.values() is", suggest_dict.values())
                print("other_player.get_hand() is", other_player.get_hand())

                for suggested_card in suggest_dict.values():
                    if suggested_card in other_player.get_hand():
                        matched_card = suggested_card
                        # print("   ",other_player.get_player_name(), "has revealed to", player.get_player_name(), matched_card)
                        # match_found = True

                        return other_player, matched_card
                    
                    else:
                        # print("No match found for", suggested_card, "in", other_player.get_player_name(), "'s hand.")
                        continue
        
                # if match_found == True:
                #     print("    Match has been found, can proceed to next turn.")
                #     break
                # else:
                #     print("    Suggest match found no matches!")
                #     #other_player = "No player has a matching card!"
                #     # matched_card = "No matched card found!"
        
        return "No player has a matching card!", "No matched card found!"
        
    #     # This method returns the list of suggestions made by a specific player.
    #     def get_suggestions_for_player(self, player):
    #         player_suggestions = []
    #         for suggestion in self.suggestions:
    #             if suggestion['player'] == player:
    #                 player_suggestions.append(suggestion)
    #         return player_suggestions
    

    # This method checks if an accusation is valid. It returns a Boolean value 
    # indicating whether or not the accusation is valid.   
    def validate_accusation(self, accusation):
        '''
        INPUT: accusation : list of three user inputs
        OUTPUT: True if accusation is valid, False otherwise
        '''
        # Precondition: accusation is cleaned up syntax to match my lists of weapons, tokens, and rooms
        has_weapon = False
        has_token = False
        has_room = False
        for guess in accusation:
            if guess in self.WEAPONS: has_weapon = True
            elif guess in self.TOKENS: has_token = True
            elif guess in self.ROOMS: has_room = True
        return has_weapon and has_token and has_room
    
    #     # This method returns the list of accusations made by a specific player.
    #     def get_accusations_for_player(self, player):
    #         player_accusations = []
    #         for accusation in self.accusations:
    #             if accusation['player'] == player:
    #                 player_accusations.append(accusation)
    #         return player_accusations

    #     # This method returns the list of cards held by a specific player.   
    #     def get_player_cards(self, player):
    #         return self.player_cards[player]

    # # create a new game
    # game = Game_processor()

    # # make a suggestion by player 1
    # game.suggestion("player1", "wrench", "study", "player2")

    # # validate the suggestion
    # is_valid = game.validate_suggestion(("player1", "wrench", "study", "player2"))
    # if is_valid:
    #     print("Valid suggestion!")
    # else:
    #     print("Invalid suggestion.")