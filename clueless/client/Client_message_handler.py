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
            return pickle.loads(self.client.recv(4096))
        except:
            pass

    def send_receive(self, data):
        #print("Player sending information to the Server")
        #print(data)
        try:
            print('...sending client -> server data')
            self.client.send(pickle.dumps(data))
            
            print('...receiving server -> client data')
            return pickle.loads(self.client.recv(4096))
        except socket.error as err:
            print(err)

    def send(self, data):
        #print("Player sending information to the Server") 
        if data:
            dic1 = pickle.dumps(data)
            try:
                self.client.send(dic1)
            except socket.error as err:
                print(err)

    def receive(self):
        #print("Player receiving information from the Server")
        rec = self.client.recv(4096)
        dic1 = pickle.loads(rec)
        if dic1:
            try:
                return dic1
            except socket.error as err:
                print(err)

    def build_client_package(self, player_id, state, contents):
        #start builing message package to send to server
        print("...building client package")
        print(f'   for player {player_id}, {state}, {contents}')
        client_package = dict({'player_id': player_id, 'turn_status': state})

        if (state == 'MOVEMENT'):
            client_package.update({'target_tile': contents})
        elif (state == 'SUGGESTION'):
            client_package.update({'suggested_cards': contents})
        elif (state == 'ACCUSATION'):
            client_package.update({'accused_cards': contents})

        return client_package
    
    def get_server_update(self):
        game_data = self.build_client_package(self.id, "get", "")
        game = self.send_receive(game_data)
        return game

    def process_server_update(self, server_message, prev_server_message):
        print(f"...processing server message --> {server_message} and prev server message {prev_server_message}")
        if server_message != prev_server_message:
            player_id = server_message['player_id']
            #player_token = server_message['player_token']
            turn_status = server_message['turn_status']

            if turn_status != "get":
                print("Player taking turn: ", player_id)
                #based on player's turn and game status, update players with the status of the game
                if turn_status == 'movement':
                    print("Player " + player_id + " chooses to move to location ", server_message['player_location'])
                    print()
                                
                elif turn_status == 'suggestion':
                    print("Player " + player_id + " suggested " + server_message['suggested_cards']['character'] + " with the " + 
                          server_message['suggested_cards']['weapon'] + " in the " + server_message['suggested_cards']['room'])
                    print()
                    #if the player client is the same as the player who made the suggestion, reveal the suggestion result
                elif turn_status == 'accusation':
                    print("Player " + player_id + " accused " + server_message['accused_cards']['character'] + " with the " + 
                        server_message['accused_cards']['weapon'] + " in the " + server_message['accused_cards']['room'])
                    print()
                    if(server_message['accuse_result'] == True):
                        print("Accusation Correct! Player " + player_id + " wins!")
                        print()
                    else:
                        print("Accusation was inccorect. Player " + player_id + " loses.")
                        print()

        #print("processed server message")
        return server_message