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
        #print("Player sending information to the Server")
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
        # print(f"Player sending information to the Server {data}") 
        if data:
            dic1 = pickle.dumps(data)
            try:
                self.client.send(dic1)
            except socket.error as err:
                print(err)
                pass

    def receive(self):
        server_update = pickle.loads(self.client.recv(4096*10))
        # print(f"...client receiving update from server {server_update}")
        # if server_update['turn_status']!='get':
        #     print(f"...client receiving update from server {server_update}")
        return server_update     

    def build_client_package(self, player_id, state, contents):
        #start builing message package to send to server
        print("...building client package")
        print(f'   for player {player_id}, {state}, {contents}')
        client_package = dict({'player_id': player_id, 'turn_status': state})

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
        
        return client_package
    
    def get_server_update(self):
        print("check get server update")
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
            if turn_status != "get":
                print("Player taking turn: ", player_id)
                #based on player's turn and game status, update players with the status of the game
                if turn_status == 'movement':
                    print(f"player {player_id} chose to move to location {server_message['player_location']}")
                
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
                    print(f"Player {player_id} accused {server_message['accused_cards']['character']} with the {server_message['accused_cards']['weapon']} in the {server_message['accused_cards']['room']}")
                    # if('accused_result_player' in server_message):
                    #     print("...accusation correct! Player " + player_id + " wins!")
                    # else:
                    #     print("...accusation incorrect. Player " + player_id + " loses.")

        # print("...processed server message")
        return server_message