from clueless.server.Tile import * 
from clueless.server.Player import *
from clueless.server.Game_processor import *
from clueless.server.Deck import Deck
from clueless.server.Player import Player

class Game:


    def __init__(self, num_players):
        # print('GAME INITIALIZED')
        self.num_players = num_players
        self.players = []
        self.dealt = False
        self.game_deck = Deck()                                 # dict for initial overall game deck
        self.case_file = self.game_deck.get_secret_deck()       # dict of three secret cards
        self.game_status = None                                 # game state of entire game
        print(f'  case_file: {self.case_file}')

        ############################
        ##### INITIALIZE TILES #####
        # to initialize an object of class tile
        # self, tile_name, tile_type, adjacent_tiles
        ############################
        #
        # INITIALIZE ROOM TILES
        # with their str name, "room", and adj tiles
        tile_study = Tile("Study", "room", ["Hallway 01", "Hallway 03", "Kitchen"])
        tile_hall = Tile("Hall", "room", ["Hallway 01", "Hallway 02", "Hallway 04"])
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
        tile_hallway_09 = Tile("Hallway 09", "hallway", ["Billiard Room", "Ballroom"])
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
        

    def get_turn_status(self):
        return self.get_turn_status

    def get_current_player(self):
        return self.get_turn_status

    def get_game_status(self):
        return self.game_status

    def get_case_file(self):
        return self.case_file
    
    def get_game_board(self):
        return self.game_board

    # NOTE: can move this to message handling later
    def get_backend_tilename(self, frontend_tilename):
        tilename_dict = {'study_room':'Study',
                         'hall':'Hall',
                         'lounge':'Lounge',
                         'library':'Library',
                         'billiard_room':'Billiard Room',
                         'dining_room':'Dining Room',
                         'conservatory':'Conservatory',
                         'ballroom':'Ballroom',
                         'kitchen':'Kitchen',
                         'hallway_1':'Hallway 01',
                         'hallway_2':'Hallway 02',
                         'hallway_3':'Hallway 03',
                         'hallway_4':'Hallway 04',
                         'hallway_5':'Hallway 05',
                         'hallway_6':'Hallway 06',
                         'hallway_7':'Hallway 07',
                         'hallway_8':'Hallway 08',
                         'hallway_9':'Hallway 09',
                         'hallway_10':'Hallway 10',
                         'hallway_11':'Hallway 11',
                         'hallway_12':'Hallway 12'}
        try:  
            return tilename_dict[frontend_tilename]
        except:
            return f"{frontend_tilename} not in dictionary!"
     
    # NOTE: can move this to message handling later
    def get_backend_playername(self, frontend_playername):
        playername_dict = {'colonel_mustard':'Colonel Mustard',
                         'miss_scarlet':'Miss Scarlet',
                         'mr_green':'Mr. Green',
                         'mrs_peacock':'Mrs. Peacock',
                         'mrs_white':'Mrs. White',
                         'prof_plum':'Professor Plum'
                         }
        try:  
            return playername_dict[frontend_playername]
        except:
            return f"{frontend_playername} not in dictionary!"
        
    # NOTE: can move this to message handling later
    def get_backend_weaponname(self, frontend_weaponname):
        weaponname_dict = {'candlestick':'Candlestick',
                         'dagger':'Dagger',
                         'lead_pipe':'Lead Pipe',
                         'revolver':'Revolver',
                         'rope':'Rope',
                         'wrench':'Wrench'
                        }
        try:  
            return weaponname_dict[frontend_weaponname]
        except:
            return f"{frontend_weaponname} not in dictionary!"
       
    # return a player whose turn it is not currently
    def get_player(self, player):
        if player in self.players:
            return self.get_player
        else:
            # unsure what we would want returned here, placeholder print
            print("That player is not in this game, please try again.")


    def get_player_object(self, player_id):
        for i, player in enumerate(self.players):
            # print(f'...comparing {player.get_player_id()} to {player_id}')
            if player.get_player_id() == player_id:
                # print(f'...returning player obj for {player.get_player_id()}')
                return player
            
    def get_first_player(self):
        #returns the id of the first player
        print("First player: " + self.players[0].get_player_id())
        return self.players[0].get_player_id()
            
    #method to add a new player object to the game
    def add_player(self, player_id, player_token):
        #print("adding new player")
        new_player = Player(player_token, player_id)

        if new_player.get_player_name() == "Miss Scarlet":
            self.players.insert(0, new_player)
        else:
            self.players.append(new_player)

        print(self.players)
        print(f'Added {new_player.get_player_name()}')



    # A method that deals a deck of cards to players 
    def deal_to_players(self)->dict:
        num_players= len(self.players)
        dealt_decks = self.game_deck.deal(num_players)
        for i, player in enumerate(self.players):
            player.set_player_hand(dealt_decks[i])
            print(f'Player {player.get_player_id()} is playing {player.get_player_name()} with hand {list(player.get_hand().keys())}')
            print()

    def set_turn_order(self):
        for i, player in enumerate(self.players):
            if i < self.num_players-1:
                player.set_next_player(self.players[i+1].get_player_id())
            else:
                #end of the list, must circle back to player one
                player.set_next_player(self.players[0].get_player_id())
            
            print("Player Name: " + player.get_player_name())
            print("Player ID: " + player.get_player_id())
            print("Next Player: " + player.get_next_player())

    ################################################################################
    # update_turn_order updates the turn order to remove the lost player
    # Input : lost_player [type: Player]
    ################################################################################
    def update_turn_order(self, lost_player):
        lost_playerid = lost_player.get_player_id() # Get string ID
        print(f'Player {lost_playerid} lost')
        for player in self.players:
            # Update player who's next player just lost to be the loser's next player
            if str(player.next_player) == lost_playerid:
                print(f'Player {player.get_player_id()}s next player updates from {lost_playerid} to {lost_player.next_player}')
                player.set_next_player(lost_player.next_player)
                break
            
    # This method determines what turn the player is taking and then routes to 
    # appropriate game logic functions to carry out turn accordingly
    def player_take_turn(self, player_turn):
        # print(" PLAYER TAKING TURN")
        '''
        INPUT: player_turn : dictionary from Game_message_handler.process_client_update(client_message)
            {'player_id': str,
            'turn_status': str,                                 # movement, accusation, or suggestion
            'next_player': str,
            'next_playername_turn': str,
            'suggested_cards': dict,                            # client_message['suggested_cards']
            'accused_cards': dict,
            'target_tile': str
            } 
            
        OUTPUT: game_status : dictionary to be sent back to the Server containing information about the turn result
            {'player_token': str,
            'turn_status': str,                   # movement, accusation, or suggestion
            'suggested_cards': dict,
            'suggested_match_card' : str,
            'suggest_result_player': str,         # Name of player who provided suggested cards, None if no matching cards were found
            'accused_cards': dict,
            'accused_result_player' : str,        # Name of player who accused correctly, None accused incorrectly
            'target_tile': str,
            'moved_player':str                    # string name of player who moved
            } 
        '''
        # Get player object
        curr_player = self.get_player_object(str(player_turn['player_id']))
        
        #  Game status stores the result of player taking a turn
        game_status = player_turn.copy()
        
        # Execute specific turn and update corresponding game_status with result
        if player_turn['turn_status'] == "movement":
            print('in player_take_turn movement')
            game_status['moved_player'] = curr_player.get_player_name()
            # backend_tilename = self.get_backend_tilename(player_turn['target_tile'])
            # target_tile_obj = self.game_board[backend_tilename]
            # print(f"  Player {curr_player.get_player_name()} chooses to move to location {target_tile_obj.get_tile_name()}")
            
            #backend_tilename = self.get_backend_tilename(player_turn['target_tile'])
            target_tile_obj = self.game_board.get(player_turn['target_tile'])
            print("target_tile_obj is", target_tile_obj)

            Game_processor.move(board_dict = self.game_board, player = curr_player, destination = target_tile_obj)
            if curr_player.get_player_old_location() is not None:
                print(f"Player {player_turn['player_id']} was on {curr_player.get_player_old_location().get_tile_name()}")
            print(f"Player {player_turn['player_id']} is now on {curr_player.get_player_current_location().get_tile_name()}")
            # game_status['move_completed'] = True
            # if move_completed_boolean is False:
            #     game_status['move_completed'] = False
            # else: 
            #     game_status['move_completed'] = True

            
        elif player_turn['turn_status'] == "accusation":
            backend_playername = self.get_backend_playername(player_turn['accused_cards']['character'])
            backend_roomname = self.get_backend_tilename(player_turn['accused_cards']['room'])
            backend_weaponname = self.get_backend_weaponname(player_turn['accused_cards']['weapon'])
            
            print(f"  Player chooses to accuse {backend_playername},{backend_weaponname},{backend_roomname}. case file is {self.case_file}")
            accuse_result = Game_processor.accuse(backend_playername, backend_weaponname, backend_roomname, self.case_file)
            if accuse_result:
                print('    Player accused correctly')
                # Include name of current player if they accused correctly
                game_status['accused_result_player'] = curr_player.get_player_name()
            else: 
                curr_player.set_player_status('LOST')
                self.update_turn_order(curr_player)
                # Force "end turn" logic since end turn button disappears after losing
                print("Player " + curr_player.get_player_id() + " is ending their turn.")
                print("Player " + curr_player.get_next_player() + " is starting their turn next.")
                game_status.update({'next_player': curr_player.get_next_player()})
                next_player_obj = self.get_player_object(curr_player.get_next_player())
                game_status.update({'next_playername_turn': next_player_obj.get_player_name()})
            
                print('    Player accused incorrectly')
            
        elif player_turn['turn_status'] == "suggestion":        
            print("  Player chooses to suggest")
            print(player_turn['suggested_cards'])


            # convert string names with megan's dict
            backend_playername = self.get_backend_playername(player_turn['suggested_cards']['character'])
            # print(backend_playername)
            backend_weaponname = self.get_backend_weaponname(player_turn['suggested_cards']['weapon'])
            # print(backend_weaponname)
            # print(curr_player)
            # print(curr_player.get_player_current_location())
            # {'character': 'mr_green', 'weapon': 'lead_pipe', 'room': None}
            # get the suggesting player's location, UPDATE ROOM ENTRY IN DICT

            # Game_processor.move(self.game_board, curr_player, self.game_board.get('Billiard Room'))

            if curr_player.get_player_current_location() is None:
                player_first_move = {
                    'Miss Scarlet' : 'Hallway 02',
                    'Professor Plum' : 'Hallway 03',
                    'Colonal Mustard' : 'Hallway 05',
                    'Mrs. Peacock' : 'Hallway 08',
                    'Mr. Green' : 'Hallway 11',
                    'Mrs. White' : 'Hallway 12'
                    }
                
                first_move_tile_name = player_first_move.get(curr_player.get_player_name())

                curr_player.update(self.game_board.get(first_move_tile_name))

                ## ADD DECREMENT IN HERE FOR TILE, OR USE MOVE DIRECTLY

            print("player is on", curr_player.get_player_current_location().get_tile_name())

            # update suggested_cards and print
            player_turn['suggested_cards']['room'] = curr_player.get_player_current_location().get_tile_name()
            #print(player_turn['suggested_cards'])
            #print("currplayer and location", curr_player.get_player_current_location())

            # remove later, input to test suggest

            suggest_dict = {'character': backend_playername,
                            'weapon': backend_weaponname,
                            'room': curr_player.get_player_current_location().get_tile_name()
            }

            # print("We made it!")
            print(suggest_dict)

            # update suggest inputs/outputs
            # suggest input currently takes: (suggest_dict, players, board_dict)
            # suggest will move players and decrement/increment tiles
            Game_processor.suggest(suggest_dict, self.players, self.game_board)

            # print("self.players is", self.players)

            # get the player's matched cards
            player_w_match, matched_card = Game_processor.get_suggest_matches_for_player(curr_player, suggest_dict, self.players)
            # TO DO: assumes output of suggest has name of player who suggested cards
            if player_w_match != "No player has a matching card!":
                game_status['suggest_result_player'] = player_w_match.get_player_name()
                game_status['suggested_match_card'] = matched_card
            else: 
                game_status['suggest_result_player'] = player_w_match
                game_status['suggested_match_card'] = matched_card
        
        #when current player has submitted that they want to end their turn
        elif player_turn['turn_status'] == 'end turn':
            print("Player " + curr_player.get_player_id() + " is ending their turn.")
            print("Player " + curr_player.get_next_player() + " is starting their turn next.")
            game_status.update({'next_player': curr_player.get_next_player()})
            next_player_obj = self.get_player_object(curr_player.get_next_player())
            game_status.update({'next_playername_turn': next_player_obj.get_player_name()})

        # print(f'... return game_status {game_status}')
        return game_status # --goes to--> server_update = Game_message_handler.build_game_package(game_status)

