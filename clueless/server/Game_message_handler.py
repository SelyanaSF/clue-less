import socket
import threading
import pickle
import sys

class Game_message_handler:

    def __init__(self):
        pass
     
    def send_game_update(conn, game_update):
        #if game_update['turn_status'] != 'pass':
            # print(f"... sending to client {game_update}")
        # indenting was wrong after if statement was moved
        conn.send(pickle.dumps(game_update))

    def receive_client_update(conn):
        client_update = pickle.loads(conn.recv(4096*10))
        # print(f"...player receiving information from the client {client_update}")
        return client_update

    def process_client_update(client_message):
        print(f"...processing client message {client_message}")
        turn_status = client_message['turn_status']
        #starting with client turn status form bc og the get condition
        player_turn = dict({'player_id': client_message['player_id'], 
                            'turn_status': turn_status,
                            'next_player': client_message['next_player'],
                            'next_playername_turn': client_message['next_playername_turn']
                            })

        if turn_status == "reset":
            pass        
        elif turn_status != "get":
            if turn_status == 'MOVEMENT':
                player_turn.update({'turn_status': 'movement'})
                player_turn.update({'target_tile': client_message['target_tile']})
                # player_turn.update({'player_token': client_message['player_token']})
                # print("hello i made it!")
            elif turn_status == 'MOVING':
                pass
                # player_turn.update({'player_token': client_message['player_token']})
            elif turn_status == 'SUGGESTION':
                player_turn.update({'turn_status': 'suggestion'})
                player_turn.update({'suggested_cards': client_message['suggested_cards']})
            elif turn_status == 'ACCUSATION':
                player_turn.update({'turn_status': 'accusation'})
                player_turn.update({'accused_cards': client_message['accused_cards']})
            elif turn_status == "chose_token": #join
                player_turn.update({'player_token': client_message['player_token']})
            elif turn_status == 'start game':
                player_turn['turn_status'] = 'get'
            elif turn_status == 'END TURN':
                player_turn.update({'turn_status': 'end turn'})
        else:
            player_turn['turn_status'] = 'pass'

        # print(f'...processed player_turn {player_turn}')
        return player_turn


    def build_game_package(game_status):
        # print("...building message package for client")
        tilename_dict = {'Study':'study_room',
                         'Hall':'hall',
                         'Lounge':'lounge',
                         'Library':'library',
                         'Billiard Room':'billiard_room',
                         'Dining Room':'dining_room',
                         'Conservatory':'conservatory',
                         'Ballroom':'ballroom',
                         'Kitchen':'kitchen',
                         'Hallway 01':'hallway_1',
                         'Hallway 02':'hallway_2',
                         'Hallway 03':'hallway_3',
                         'Hallway 04':'hallway_4',
                         'Hallway 05':'hallway_5',
                         'Hallway 06':'hallway_6',
                         'Hallway 07':'hallway_7',
                         'Hallway 08':'hallway_8',
                         'Hallway 09':'hallway_9',
                         'Hallway 10':'hallway_10',
                         'Hallway 11':'hallway_11',
                         'Hallway 12':'hallway_12'}
        
        game_package = dict({
            'player_id': game_status['player_id'],
            # 'player_token': game_status['player_token'],
            'turn_status': game_status['turn_status'],
            'next_player': game_status['next_player'],
            'next_playername_turn': game_status['next_playername_turn']
        })

        turn_status = game_package['turn_status']

        #based on game status, build a package for the game status message
        if turn_status != "get":
            if turn_status == 'movement':
                frontend_tilename = tilename_dict[(game_status['target_tile'])]
                game_package.update({'player_location': frontend_tilename})
                # game_package.update({'player_location': game_status['target_tile']})
                game_package.update({'moved_player': game_status['moved_player']})
                print(game_package)
            elif turn_status == 'MOVING':
                game_package.update({'valid_tile_names_for_player': game_status['valid_tile_names_for_player']})
                
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
                    
            elif turn_status == 'end turn':
                game_package.update({'next_player': game_status['next_player']})
                game_package.update({'next_playername_turn': game_status['next_playername_turn']})
                
            elif turn_status == 'start game':
                game_package.update({'next_player': game_status['next_player']})
                game_package.update({'next_playername_turn': game_status['next_playername_turn']})
                        
            elif turn_status == 'chose token':
                game_package.update({'next_player': game_status['next_player']})
                
        else:
            game_package.update({'turn_status': 'pass'})
        

        #print(f'...built message package for client{game_package}')
        return game_package

    def broadcast(clients, message):
        # print(f'...broadcasting {message} to this many clients: {len(clients)}')

        # client is same as conn
        for client in clients:
            # if message["turn_status"] == "MOVING":
            #     print(f"i am client {client}")
            try: 
                Game_message_handler.send_game_update(client, message)
            except Exception as err:
                print(f'failed broadcast with error {err}')
                # pass
