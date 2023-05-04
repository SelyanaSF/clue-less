# #Multi-Client Network Module
import socket
import pickle
import threading
import sys

HOST_ADDR = socket.gethostbyname(socket.gethostname())
HOST_PORT = 8080

class Client_message_handler:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = HOST_ADDR
        self.port = HOST_PORT
        self.addr = (self.server, self.port)
        self.id = self.connect()
        self.game_has_started = False
        self.player_moved = False
        self.player_suggested = False
        self.player_accused = False
        self.player_ended_turn = False
        self.player_taking_turn = False

    def get_id(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(4096*10))
        except socket.error as err:
            print(err)
            pass

    def send_receive(self, data):
        # print("Player sending information to the Server")
        #print(data)
        try:
            # print('...sending client -> server data
            # ')
            self.client.send(pickle.dumps(data))
            
            # print('...receiving server -> client data')
            return pickle.loads(self.client.recv(4096*10))
        except socket.error as err:
            print(err)
            pass

    def send(self, data):
        # print(f"... Player sending information to the Server {data}") 
        if data:
            dic1 = pickle.dumps(data)
            try:
                self.client.send(dic1)
            except socket.error as err:
                print(f'failed to send with error {err}')
                pass

    def receive(self):
        server_update = pickle.loads(self.client.recv(4096*10))
        # print(f"...client receiving update from server {server_update}")
        # if server_update['turn_status']!='get':
        #     print(f"...client receiving update from server {server_update}")
        return server_update     

    def build_client_package(self, player_id, state, contents, next_player, next_playername_turn):
        #start builing message package to send to server
        # print("...building client package")
        # print(f'   for player {player_id}, {state}, {contents}')
        client_package = dict({'player_id': player_id, 
                               'turn_status': state,
                               'next_player': '', 
                               'next_playername_turn':''
                               })

        if (state == 'MOVEMENT'):
            client_package.update({'target_tile': contents})
            # print("updated client package!")
        # elif (state == 'MOVING'):
        #     client_package.update({'player_token': contents})
        elif (state == 'SUGGESTION'):
            client_package.update({'suggested_cards': contents})
        elif (state == 'ACCUSATION'):
            client_package.update({'accused_cards': contents})
        elif (state == 'chose_token'): # join
            client_package.update({'player_token': contents})
        elif (state == "END TURN"):
            # pass
            print(f'... built client package {client_package}')
            return client_package
            
        return client_package
    
    def get_server_update(self):
        # print("check get server update")
        game_data = self.build_client_package(self.id, "get", "")
        game = self.send_receive(game_data)
        return game

    # TO DO: move and suggest
    def process_server_update(self, server_message, prev_server_message):
        # print(f"...processing server message --> {server_message} and prev server message {prev_server_message}")
        player_id = server_message['player_id']
        # player_token = server_message['player_token']
        turn_status = server_message['turn_status']
        
        if server_message != prev_server_message:
            # print(f"...processing server message --> {server_message} and prev server message {prev_server_message}")
            if turn_status != "get" and turn_status != 'pass':
                if not self.player_taking_turn:
                    print("Player taking turn: ", player_id)
                    self.player_taking_turn = True
                #based on player's turn and game status, update players with the status of the game
                if turn_status == 'movement':
                    if not self.player_moved:
                      print(f"player {player_id} chose to move to location {server_message['player_location']}")
                      self.player_moved = True
                
                # from the server message, get the player id of the player moving and print the list of room
                # options provided from the server as a list
                elif turn_status == 'MOVING':
                    print(f"    Player {player_id} has these room options available!")
                    print(f"    {server_message['valid_tile_names_for_player']}")

                elif turn_status == 'suggestion':
                    print("Player " + player_id + " suggested " + server_message['suggested_cards']['character'] + " with the " + 
                            # server_message['suggested_cards']['weapon'])
                            server_message['suggested_cards']['weapon'] + " in the " + server_message['suggested_cards']['room'])
                    #if the player client is the same as the player who made the suggestion, reveal the suggestion result
                    # if 'suggest_result_player' in server_message:
                    #     print(server_message['suggest_result_player'], "has shown you:", server_message['suggested_match_card'])
                    # else:
                    #     print("No match found amongst other hands!")

                    if 'suggest_result_player' in server_message and server_message['suggested_match_card'] != "No matched card found!":
                        print(server_message['suggest_result_player'], "is showing Player", player_id, "a card from their hand! How intriguing :)")
                    else:
                        print("No match found amongst other hands!")

                elif turn_status == 'accusation':
                    if not self.player_accused:
                        print(f"Player {player_id} accused {server_message['accused_cards']['character']} with the {server_message['accused_cards']['weapon']} in the {server_message['accused_cards']['room']}")
                        # if('accused_result_player' in server_message):
                        #     print("...accusation correct! Player " + player_id + " wins!")
                        # else:
                        #     print("...accusation incorrect. Player " + player_id + " loses.")
                        self.player_accused = True
                elif turn_status == 'end turn':
                    print('... in Client_msg_handler')
                    if not self.player_ended_turn:
                        next_player_id = server_message['next_player']
                        print("Player " + player_id + "'s turn ended.")
                        self.player_ended_turn = True

                        if next_player_id == self.id:
                            print("It is now your turn!")
                        else:
                            print(f"It is now Player {next_player_id}'s turn.")
                            self.player_moved = False
                            self.player_suggested = False
                            self.player_accused = False
                            self.player_ended_turn = False
                            self.player_taking_turn = False
                        print()

                elif turn_status == 'start game':
                    if not self.game_has_started:
                        print("Game has begun. Let's play ClueLess!")
                        print("Player " + server_message['next_player'] + " starts")
                        print()
                        self.game_has_started = True
                        
                elif turn_status == 'START':
                    print(server_message)
                else:
                    server_message['turn_status'] = 'pass'

        prev_server_message = server_message
        # print("...processed server message")
        return server_message
    
    def get_readable_tilename(frontend_tilename):
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
        try: return tilename_dict[frontend_tilename]
        except: return f"{frontend_tilename} not in dictionary!"
     
    def get_readable_playername(frontend_playername):
        playername_dict = {'colonel_mustard':'Colonel Mustard',
                         'miss_scarlet':'Miss Scarlet',
                         'mr_green':'Mr. Green',
                         'mrs_peacock':'Mrs. Peacock',
                         'mrs_white':'Mrs. White',
                         'prof_plum':'Professor Plum'
                         }
        try:  return playername_dict[frontend_playername]
        except: return f"{frontend_playername} not in dictionary!"
        
    def get_readable_weaponname(frontend_weaponname):
        weaponname_dict = {'candlestick':'Candlestick',
                         'dagger':'Dagger',
                         'lead_pipe':'Lead Pipe',
                         'revolver':'Revolver',
                         'rope':'Rope',
                         'wrench':'Wrench'
                        }
        try:  return weaponname_dict[frontend_weaponname]
        except: return f"{frontend_weaponname} not in dictionary!"