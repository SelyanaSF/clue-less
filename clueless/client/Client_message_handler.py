# #Multi-Client Network Module
import socket
import pickle
import threading

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
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as err:
            print(err)

    def send(self, data):
        #print("Player sending information to the Server")
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as err:
            print(err)

    def receive(self):
        #print("Player receiving information from the Server")
        try:
            return pickle.loads(self.client.recv(4096))
        except socket.error as err:
            print(err)

    def build_package(self, state, contents):
        status = state
        package = dict({'header': status, 'player_id': self.id, 'data': contents})
        return package
    
    def get_server_update(self):
        game_data = self.build_package("get", "")
        game = self.send_receive(game_data)
        return game

    def process_server_update(self, game, prev_game_state):
        #print("processing server message")
        if game != prev_game_state:
            #print(game)
            game_player_id = game['player_token']
            game_player_status = game['turn_status']
            #game_player_turn = game['player_turn_details']

            if game_player_status == 'CHOOSING':
                print("Player taking turn: Player ", game_player_id)
                #print("Player chooses to move to location ", game_player_turn)
                print()

        return game