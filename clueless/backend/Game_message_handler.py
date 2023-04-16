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
        player_turn = dict()
        player_status = player_data['header']
        player_id = player_data['player_id']
        #print(status)

        if player_status == "reset":
            pass        
        elif player_status != "get":
            player_details = player_data['data']

            player_turn['player_turn_id'] = player_id
            player_turn['player_turn_type'] = player_status
            player_turn['player_turn_details'] = player_details

        return player_turn


    def build_game_package():
        pass