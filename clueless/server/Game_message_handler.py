import pickle

class Game_message_handler:

    def __init__(self):
        pass

    def send_game_update(conn, game_update):
        conn.send(pickle.dumps(game_update))

    def receive_client_update(conn):
        client_update = pickle.loads(conn.recv(4096))
        return client_update

    def process_client_update(player_data):
        #print("processing client message")
        player_turn = {}
        player_status = player_data['header']
        player_id = player_data['player_id']

        if player_status == "reset":
            pass        
        elif player_status == "get":
            player_turn['player_token'] = player_id
            player_turn['turn_status'] = 'skip'
        else:
            player_turn['player_token'] = player_id
            player_turn['turn_status'] = player_status

        #print(player_turn)
        return player_turn


    def build_game_package(game_status):
        pass