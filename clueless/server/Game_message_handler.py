import socket
import threading
import pickle
import sys

class Game_message_handler:

    def __init__(self):
        pass

    def send_game_update(conn, game_update):
        # print(f"... sending to client {game_update}")
        conn.send(pickle.dumps(game_update))

    def receive_client_update(conn):
        client_update = pickle.loads(conn.recv(4096))
        # print(f"...player receiving information from the client {client_update}")
        return client_update

    def process_client_update(client_message):
        # print(f"...processing client message {client_message}")
        turn_status = client_message['turn_status']
        #starting with client turn status form bc og the get condition
        player_turn = dict({'player_id': client_message['player_id'], 'turn_status': turn_status})

        if turn_status == "reset":
            pass        
        elif turn_status != "get":
            if turn_status == 'MOVEMENT':
                player_turn.update({'turn_status': 'movement'})
                player_turn.update({'target_tile': client_message['target_tile']})
            elif turn_status == 'SUGGESTION':
                player_turn.update({'turn_status': 'suggestion'})
                player_turn.update({'suggested_cards': client_message['suggested_cards']})
            elif turn_status == 'ACCUSATION':
                player_turn.update({'turn_status': 'accusation'})
                player_turn.update({'accused_cards': client_message['accused_cards']})

        # print(f'...processed player_turn {player_turn}')
        return player_turn


    def build_game_package(game_status):
        # print("...building message package for client")
        game_package = dict({
            'player_id': game_status['player_id'],
            #'player_token': game_status['player_token'],
            'turn_status': game_status['turn_status']
        })

        turn_status = game_package['turn_status']

        #based on game status, build a package for the game status message
        if turn_status != "get":
            if turn_status == 'movement':
                game_package.update({'player_location': game_status['target_tile']})
            elif turn_status == 'suggestion':
                game_package.update({'suggested_cards': game_status['suggested_cards']})
                # game_package.update({'suggest_result': game_status['suggest_result']})
                if 'suggested_match_card' in game_status:
                    game_package.update({'suggest_result_player': game_status['suggest_result_player']})
                # game_package.update({'suggested_player_location': game_status['suggested_cards']['room']})
                if 'suggested_match_card' in game_status:
                    game_package.update({'suggested_match_card': game_status['suggested_match_card']})
            elif turn_status == 'accusation':
                game_package.update({'accused_cards': game_status['accused_cards']})
                if 'accused_result_player' in game_status:
                    game_package.update({'accused_result_player': game_status['accused_result_player']})

        # print(f'...built message package for client{game_package}')
        return game_package
