# Game Module
from clueless.client.Client_message_handler import Client_message_handler
from clueless.server.Deck import Deck
from clueless.client.Weapon_image import Weapon_Image
from clueless.client.Splash_Button import Splash_Button
from clueless.client import Button, Client_game_board
from pathlib import Path
import pickle
import pygame, sys
import threading
import random

from datetime import datetime
import time
import traceback

DEFAULT_GAME = dict({'player_id': '0', 'turn_status': 'get','next_player':'0','next_playername_turn':''})
server_update = dict({})
CHARACTER_TOKENS = ["Mrs. Peacock", "Mrs. White", "Miss Scarlet", "Mr. Green", "Colonel Mustard", "Professor Plum"]
data_folder = Path("clueless/data/graphics/")

class Game_controller:

    # WIDTH AND HEIGHT OF THE WINDOW
    WIDTH = 1050
    HEIGHT = 700
    FPS = 20

    # There are NINE Game State : "START", "MOVING", "ACCUSING", "SUGGESTING", "CHOOSING_TOKEN", "SPLASH_SCREEN", "chose_token", "ask hand", "MOVEMENT"
    # Each State will have different views
    # SEND MESSAGE TO SERVER comments are placeholder where the code sends message to server
    ############################################################################################
    # game_loop is the function to keep looping check_events as long as playing=True
    # check_events is the function to check user's mouse movement
    # add_main_view is the function to show main view
    # add_suggest_view is the function to show suggest view
    # add_accuse_view is the function to show accuse view


    def __init__(self):
        pygame.init()
        
        self.network = Client_message_handler()
        self.id = int(self.network.get_id())
        self.player_id = str(self.id)
        self.playing = True
        player_caption = "Clue-Less Player " + self.player_id
        pygame.display.set_caption(player_caption)
        self.game_state = DEFAULT_GAME
        self.player_token = 'None'
        self.state = "SPLASH_SCREEN"
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.base_color = self.randomise_color()
        self.token_coor_dict = {}
        self.tiles_directory = {}
        self.screen.fill(self.base_color)
        self.clock = pygame.time.Clock()
        self.board = Client_game_board.Client_game_board()
        self.character_choice = None
        self.weapon_choice = None
        self.room_choice = None
        self.lost = False
        self.on_playerid_turn = 0
        self.on_playername_turn = ''
        self.first_move_complete = False
        self.end_turn_received = False
        self.game_loop()

    ################################################################################
    # game_loop is the function to keep looping check_events as long as playing=True
    ################################################################################
    def game_loop(self):

        prev_game_state = DEFAULT_GAME
        print("You are Player ", self.id)
        self.game_state['player_id'] = self.player_id
        self.game_state['player_token'] = self.player_token
        self.game_state['turn_status'] = "get"

        input_tile_name = ''

        game_data = self.network.build_client_package(self.player_id, "join", self.player_token, '','') # 'next_player': '', 'next_playername_turn':''
        # game_data = self.network.build_client_package(self.player_id, "join", self.player_token)
        self.network.send(game_data)

        while self.playing:
            self.tick()
            self.render()

            try:
                #game_update = self.network.get_server_update()
                current_time = datetime.now() 
                # print("....current Time =", current_time)
                
                #if game_data != prev_game_data:
                self.network.send(game_data)
                # print("...sent client message")
                #  prev_game_data = game_data

                try:
                    game = self.network.receive()
                except Exception as err:
                    print("Couldn't receive server update")
                    # print(type(err))
                    # print(err)
                    # break
                # game = self.network.receive()
                # print(f'......{game} ')
                # print(f'......{game_data} ')      
                                                      
                # if game['player_id'] != self.player_id:
                #     print(f"... received from different player { game['player_id']}")   
                try:
                    prev_game_state = self.network.process_server_update(game, prev_game_state)
                    
                    if prev_game_state['turn_status'] == 'accusation' or prev_game_state['turn_status'] == 'movement' or prev_game_state['turn_status'] == 'suggestion':
                        self.update_views(prev_game_state)
                        self.end_turn_received = False
                        
                    elif prev_game_state['turn_status'] == 'start game' and self.first_move_complete == False:
                        self.first_move_complete = True # Ensure this only updates once, doesn't interfere with end turn later
                        # print('Game_controller: updating player turn')
                        self.end_turn_received = False
                        self.on_playerid_turn = prev_game_state['next_player']
                        self.on_playername_turn = prev_game_state['next_playername_turn']
                        print("Player taking turn: ", self.on_playername_turn)
                    # END TURN finished
                    elif prev_game_state['turn_status'] == 'end turn':
                        prev_player = self.on_playerid_turn
                        #self.state = 'START'
                        # Update player turn to next player
                        self.on_playerid_turn = prev_game_state['next_player']
                        self.on_playername_turn = prev_game_state['next_playername_turn']
                        
                        if not self.end_turn_received:
                            print(f"Player {prev_player} ended their turn.")
                            if self.on_playerid_turn == self.player_id:
                                print(f"It's your turn!")
                            else:
                                print(f"It's {self.on_playername_turn}'s turn")
                            self.end_turn_received = True
                        # print(f'prev_game_state is now {prev_game_state}')
                          
                except:
                    print("Couldn't process_server_update")
                    break

            except:
                run = False
                print("Couldn't get game")
                break

            events = pygame.event.get()
            # print("events is", events)
            # print(f'... checkin events {prev_game_state}')
            game_data = self.check_events(events, prev_game_state)
            # print(f'game_data is now {game_data}')
            # print()
            
        # when pygame.QUIT event happens, change self.playing to False 
        # the while loop will end and quit the game
        pygame.quit()

    ################################################################################
    # check_events is the function to check user's mouse movement
    # Input : events [type: Pygame Event]
    ################################################################################
    def check_events(self, events, prev_game_state) :
        # print('...checking events')
        mousePos = pygame.mouse.get_pos()
        turn_data = DEFAULT_GAME
        for event in events:
            if event.type == pygame.QUIT:
                self.playing = False

            if (self.state == 'SPLASH_SCREEN'):
                self.add_splash_screen(events)

            if (self.state == 'START'):
                # print("check_events start")
                # self.message_for_server = {}
                self.room_choice = None
                self.screen.fill(self.base_color)
                turn_data = self.add_main_view(events, prev_game_state)
            # This is to highlight rectangle when choosing the room and print the choosen one on the options box

            if (self.state == 'CHOOSING_TOKEN'):
                self.choose_player_token(events)
            
            if (self.state == 'MOVING' and 'valid_tile_names_for_player' in prev_game_state): #'MOVEMENT'):
                # print("check_events moving")
                turn_data = self.add_main_view(events, prev_game_state)
                allowed_tiles = []

                # TRANSLATE tile name
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
                
                for each in prev_game_state['valid_tile_names_for_player']:
                    allowed_tiles.append(tilename_dict[each])

                self.board.highlight_tile_rect(self.screen,(0,100,0), allowed_tiles)

                # print the valid rooms in the bottom lefthand corner of the window
                message_font_02 = pygame.font.SysFont('Comic Sans MS', 20)
                message_surface_02 = message_font_02.render("Valid rooms: " + str(allowed_tiles), False, (120,39,64), (202, 228, 241))
                #print("Valid rooms: " + str(prev_game_state.get('valid_tile_names_for_player')))
                # message_surface_rect_02 = message_surface_02.get_rect(topleft = (100,750))
                self.screen.blit(message_surface_02, (100,650))

                # Only allow event clicked for tiles listed on prev_game_state array

                for key in allowed_tiles:
                    if (self.tiles_directory[key][0].collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                        pygame.draw.rect(self.screen, (202, 228, 241), (800,450,180,50), width=0, border_radius=5)
                        self.board.highlight_tile_rect(self.screen,(0,200,0),[key])
                        message_font = pygame.font.SysFont('Comic Sans MS', 14)
                        message_surface = message_font.render( key + '.  Proceed?', False, (120,39,64))
                        message_surface_rect = message_surface.get_rect(topleft = (810, 450))
                        self.screen.blit(message_surface, message_surface_rect)
                        self.room_choice = key

                        # pygame.draw.rect(self.screen, (202, 228, 241), (800,450,180,50), width=0, border_radius=5)
                        # self.board.highlight_tile_rect(self.screen,(0,200,0),key)
                        # message_font_02 = pygame.font.SysFont('Comic Sans MS', 20)
                        # message_surface_02 = message_font_02.render("Valid rooms: " + str(prev_game_state.get('valid_tile_names_for_player')), False, (120,39,64), (202, 228, 241))
                        # print("Valid rooms: " + str(prev_game_state.get('valid_tile_names_for_player')))
                        # # message_surface_rect_02 = message_surface_02.get_rect(topleft = (100,750))
                        # self.screen.blit(message_surface_02, (100,650))

                enterRect = pygame.Rect(810, 560, 60, 35)
                if (enterRect.collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                    if self.room_choice is not None:
                        self.state = "MOVING"
                        # SEND MESSAGE TO SERVER AND MOVE TOKEN
                        turn_data = self.network.build_client_package(self.player_id, "MOVEMENT", self.room_choice, '','') # 'next_player': '', 'next_playername_turn':''
                        self.state = "MOVEMENT"
                        self.move_token(self.player_token, self.tiles_directory[self.room_choice][1])
                        # self.network.send(turn_data)
                        #print("turn_data is", turn_data)
                        #print(f"sending message to server for movement: {self.player_id}, {self.state}, {self.room_choice}")
                        self.state = 'START'

                #Manually record the rectangle position of close button. Everytime this button is pressed, close the options box
                closeRect = pygame.Rect(970, 570, 25, 25)
                if (closeRect.collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                    self.board.close_room_options(self.screen, self.base_color)
                    self.state = "START"
                    #is_Room_Selection_Active = False

            if (self.state == 'SUGGESTING'):
                suggested_card_dict = self.add_suggest_view(events)

                for key in self.suggest_weapon_dict:
                    if self.suggest_weapon_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.suggest_weapon_dict[key][2],key)
                    if (self.suggest_weapon_dict[key][0].collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                        for i in self.suggest_weapon_dict:
                            self.suggest_weapon_dict[i][3] = False
                        if (self.suggest_weapon_dict[key][2] == 'weapon') :
                            # print('Player choose weapon: ' + key)
                            self.suggest_weapon_dict[key][3] = True
                            self.weapon_choice = key

                for key in self.suggest_suspect_dict:
                    if self.suggest_suspect_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.suggest_suspect_dict[key][2],key)
                    if (self.suggest_suspect_dict[key][0].collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                        for i in self.suggest_suspect_dict:
                            self.suggest_suspect_dict[i][3] = False
                        if (self.suggest_suspect_dict[key][2] == 'suspect') :
                            # print('Player choose suspect: ' + key)
                            self.suggest_suspect_dict[key][3] = True
                            self.character_choice = key

                turn_data = self.network.build_client_package(self.player_id, self.state, suggested_card_dict, '','') # 'next_player': '', 'next_playername_turn':''

            if (self.state == 'ACCUSING'): #'ACCUSATION'):
                accused_card_dict = self.add_accuse_view(events)
                
                for key in self.accuse_weapon_dict:
                    if self.accuse_weapon_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.accuse_weapon_dict[key][2],key)
                    if (self.accuse_weapon_dict[key][0].collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                        for i in self.accuse_weapon_dict:
                            self.accuse_weapon_dict[i][3] = False
                        if (self.accuse_weapon_dict[key][2] == 'weapon') :
                            # print('Player choose weapon: ' + key)
                            self.accuse_weapon_dict[key][3] = True
                            self.weapon_choice = key

                for key in self.accuse_suspect_dict:
                    if self.accuse_suspect_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.accuse_suspect_dict[key][2],key)
                    if (self.accuse_suspect_dict[key][0].collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                        for i in self.accuse_suspect_dict:
                            self.accuse_suspect_dict[i][3] = False
                        if (self.accuse_suspect_dict[key][2] == 'suspect') :
                            # print('Player choose suspect: ' + key)
                            self.accuse_suspect_dict[key][3] = True
                            self.character_choice = key

                for key in self.accuse_room_dict:
                    if self.accuse_room_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.accuse_room_dict[key][2],key)
                    if (self.accuse_room_dict[key][0].collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                        for i in self.accuse_room_dict:
                            self.accuse_room_dict[i][3] = False
                        if (self.accuse_room_dict[key][2] == 'room') :
                            # print('Player choose room: ' + key)
                            self.accuse_room_dict[key][3] = True
                            self.room_choice = key
                # # Testing receive here
                # turn_data = self.network.receive()
                # print(f"receiving message from server after accusation: {turn_data}")
                turn_data = self.network.build_client_package(self.player_id, self.state, accused_card_dict, '','') # 'next_player': '', 'next_playername_turn':''
            if (self.state == 'ask hand' and 'player_hand' in prev_game_state):
                self.add_hands_view(prev_game_state['player_hand'])

            # HERE is this needed?
            # if (self.state == 'END TURN'):
            #     self.state == "START"
            #     turn_dict = {'':''}
            #     turn_data = self.network.build_client_package(self.player_id, self.state, turn_dict, '','') # 'next_player': '', 'next_playername_turn':''
                # print(f'... turn data is now {turn_data}')
                
        return turn_data

    ################################################################################
    # add_main_view is the function to show main view
    # Input : events [type: Pygame Event]
    ################################################################################
    def add_main_view(self, events, prev_game_state):     
        if self.on_playerid_turn == 0:
            self.board.display_update(self.screen, '', (300, 30))
        elif self.on_playerid_turn == self.player_id:
            self.board.display_update(self.screen, f"It's your turn", (300, 30))
        else:
            self.board.display_update(self.screen, f"It's {self.on_playername_turn}'s turn", (300, 30))
                
        player_caption = "Clue-Less Player " + str(self.id) + ": " + str(self.player_token)
        pygame.display.set_caption(player_caption)
        # Add board
        self.board.load_tiles(self.screen, self.board)
        self.tiles_directory = self.board.get_tiles_directory()
        turn_data = DEFAULT_GAME

        # Initialize Buttons
        button_Y_Pos = 75
        button_X_Pos = 800
        button_distance = 60
        is_Room_Selection_Active = self.board.load_button(self.screen, "Go To Room", button_X_Pos, button_Y_Pos, (150, 150, 150))
        is_Suggest_Selection_Active = self.board.load_button(self.screen, "Suggest", button_X_Pos, button_Y_Pos + button_distance,(150, 150, 150))
        is_Accuse_Selection_Active = self.board.load_button(self.screen, "Accuse", button_X_Pos, button_Y_Pos + button_distance*2,(150, 150, 150))
        isEndTurnSelectionActive = self.board.load_button(self.screen, "End Turn", button_X_Pos, button_Y_Pos + button_distance*3,(150, 150, 150))

        is_Show_Hands_Active = self.board.load_button(self.screen, "My Cards", button_X_Pos, button_Y_Pos + button_distance*4.5, (205,200,177))
            
        # Initialize valid players 
        # TO DO: players should be added to screen later depending on which tokens are chosen (here for now to test)
        self.token_coor_dict = self.board.load_player_tokens(self.screen, self.board, self.token_coor_dict)
                
        mousePos = pygame.mouse.get_pos()
        if is_Room_Selection_Active:
            # self.state = "MOVEMENT"
            self.state = "MOVING"
            self.board.load_options(self.screen, self.state, events)
            print('Player chose to move')
            # This data stores the mouse position of the button
            #turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos))
            turn_data = self.network.build_client_package(self.player_id, self.state, self.player_token, '','') # 'next_player': '', 'next_playername_turn':''
            self.network.send(turn_data)

        if is_Accuse_Selection_Active:
            # self.state = "ACCUSATION"
            self.state = "ACCUSING"
            self.board.load_options(self.screen, self.state, events)
            turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos), '','') # 'next_player': '', 'next_playername_turn':''
            #print(turn_data)
            self.network.send(turn_data)

        if is_Suggest_Selection_Active:
            self.state = "SUGGESTING"
            self.board.load_options(self.screen, self.state, events)
            turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos), '','') # 'next_player': '', 'next_playername_turn':''
            #print(turn_data)
            self.network.send(turn_data)
        
        if is_Show_Hands_Active:
            self.state = "ask hand"
            turn_data = self.network.build_client_package(self.player_id, self.state, self.player_token, '','') # 'next_player': '', 'next_playername_turn':''
            self.network.send(turn_data)

        # if player chooose end turn, then it passes the turn to others.
        if isEndTurnSelectionActive:
            self.state = "END TURN"
            self.board.load_options(self.screen, self.state, events)
            turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos), '','') # 'next_player': '', 'next_playername_turn':''
            # #print(turn_data)
            self.network.send(turn_data)
            self.state = 'START'
        if self.lost == True:
            self.board.display_update(self.screen, "Sorry, You Lost!", (300, 30))
            board_surface = pygame.Surface((2000,2000))
            board_surface.fill('gray')
            board_surface.set_alpha(200)
            self.screen.blit(board_surface,(0,0))
            
        return turn_data

    ################################################################################
    # add_suggest_view is the function to show suggest view
    # Input : events [type: Pygame Event]
    ################################################################################
    def add_suggest_view(self, events):
        suggested_card_dict = {}
        pygame.display.set_caption("Suggest Player : ")
        self.screen.fill(self.base_color)
        self.suggest_weapon_dict = self.board.get_weapon_directory()
        self.suggest_suspect_dict = self.board.get_suspect_directory()

        # Initialize Back Button
        button_X_Pos = 250
        button_Y_Pos = 620
        button_color = (150, 150, 150)
        is_back_button_active = self.board.load_button(self.screen, "Back to Main", button_X_Pos, button_Y_Pos, button_color)
        is_submit_button_active = self.board.load_button(self.screen, "Submit", button_X_Pos+350, button_Y_Pos, button_color)

        self.board.load_suggest_board(self.screen, self.board)
        self.board.load_options(self.screen, self.state, events)
        if is_back_button_active:
            self.reset_weapon_and_suspect_dict(self.state)
            self.state = "START"
            self.screen.fill(self.base_color)

        if is_submit_button_active:
            self.reset_weapon_and_suspect_dict(self.state)
            self.state = "SUGGESTION"
            self.screen.fill(self.base_color)
            # SEND MESSAGE TO SERVER
            print('Sending message to server for suggestion: ')
            suggested_card_dict = {'character':self.character_choice,
                                    'weapon':self.weapon_choice}
                                    #'room': None}
            print("this is suggested card dict", suggested_card_dict)

            # turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos))
            #print(turn_data)
            # self.network.send(turn_data)

        return suggested_card_dict

    ################################################################################
    # add_accuse_view is the function to show accuse view
    # Input : events [type: Pygame Event]
    ################################################################################
    def add_accuse_view(self, events):
        accused_card_dict = {}
        pygame.display.set_caption("Accuse Player : ")
        self.screen.fill(self.base_color)
        self.accuse_weapon_dict = self.board.get_weapon_directory()
        self.accuse_suspect_dict = self.board.get_suspect_directory()
        self.accuse_room_dict = self.board.get_room_directory()
        
        # Initialize Back Button
        button_X_Pos = 250
        button_Y_Pos = 620
        button_color = (150, 150, 150)
        is_back_button_active = self.board.load_button(self.screen, "Back to Main", button_X_Pos, button_Y_Pos, button_color)
        is_submit_button_active = self.board.load_button(self.screen, "Submit", button_X_Pos+350, button_Y_Pos, button_color)

        self.board.load_accuse_board(self.screen, self.board)
        if is_back_button_active: 
            self.reset_weapon_and_suspect_dict(self.state)
            self.state = "START"
            self.screen.fill(self.base_color)

        if is_submit_button_active:
            self.reset_weapon_and_suspect_dict(self.state)
            self.state = "ACCUSATION" #START"
            self.screen.fill(self.base_color)
            # SEND MESSAGE TO SERVER
            accused_card_dict = {'character':self.character_choice,
                                 'weapon':self.weapon_choice,
                                 'room':self.room_choice}
            # turn_data = self.network.build_client_package(self.player_id, self.state, accused_card_dict)
        return accused_card_dict
            # # self.network.send(turn_data)
            # print(f"game_controller ... sending message to server for accusation: {accused_card_dict}")
            # game = self.network.send_receive(turn_data)
            # print(f"game_controller ... receiving message from server for accusation: {game}")
    
    ################################################################################
    # update_views is the function to read the processed game state and update views correspondingly
    # Input : prev_game_state [type: dict]
    ################################################################################
    def update_views(self, prev_game_state):
        this_player_id = prev_game_state['player_id']
        
        # ACCUSATION finished
        if prev_game_state['turn_status']=='accusation':
            if 'accused_result_player' not in prev_game_state:
                if this_player_id == self.player_id:
                    print("You Lost!")
                    self.lost = True
                    self.board.display_update(self.screen, "Sorry, You Lost!", (300, 30))
                else:
                    print(f"Player {this_player_id} Lost!")
                    self.board.display_update(self.screen, f"Player {this_player_id} Lost!", (300, 30))
                # Player lost, update turn
                self.on_playerid_turn = prev_game_state['next_player']
                self.on_playername_turn = prev_game_state['next_playername_turn']
                self.state = 'START'
                # Below is essential to reset the state to START so old messages don't glitch
                turn_data = self.network.build_client_package(self.player_id, self.state, '', '','') # 'next_player': '', 'next_playername_turn':''
                self.network.send(turn_data)

            else: 
                self.state = 'WIN'
                this_player_id = prev_game_state['player_id']
                if this_player_id == self.player_id:
                    self.add_win_screen(winner=True, winner_player_id=this_player_id, case_file=prev_game_state['accused_cards'])
                    print("You Won!")
                else:
                    self.add_win_screen(winner=False, winner_player_id=this_player_id, case_file=prev_game_state['accused_cards'])
                    print(f"Player {this_player_id} Won!")
            
        # MOVEMENT finished
        # player_location: holds front end tilename
        # moved_player: holds front end and back end names (same)
        elif prev_game_state['turn_status'] == 'movement':
            print(f"Success! Player {prev_game_state['player_id']} has moved to {prev_game_state['player_location']}!")    
            self.move_token(prev_game_state['moved_player'], self.tiles_directory[prev_game_state['player_location']][1])
            print("moved_player is", prev_game_state['moved_player'])
            #print(self.tiles_directory[prev_game_state['player_location']][1])
            #print(self.player_token)
            #game_data = self.network.build_client_package(self.player_id, 'get', self.player_token)
            if this_player_id == self.player_id:
                # TO DO better way of displaying text instead of blit
                self.board.display_update(self.screen, f"You've successfully moved to {prev_game_state['player_location']}!", (300, 30))
            else:
                self.board.display_update(self.screen, f"{prev_game_state['moved_player']} has moved to {prev_game_state['player_location']}", (300, 30))
            self.state = 'START'
            turn_data = self.network.build_client_package(self.player_id, self.state, '', '','') # 'next_player': '', 'next_playername_turn':''
            self.network.send(turn_data)

        # SUGGEST finished
        elif prev_game_state['turn_status'] == 'suggestion' and 'suggested_cards' in prev_game_state:
            print(f"Success! Player {prev_game_state['player_id']} has suggested {prev_game_state['suggested_cards']}!")
            
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
            
            frontendname_dict = {'colonel_mustard':'Colonel Mustard',
                         'miss_scarlet':'Miss Scarlet',
                         'mr_green':'Mr. Green',
                         'mrs_peacock':'Mrs. Peacock',
                         'mrs_white':'Mrs. White',
                         'prof_plum':'Professor Plum'
                         }

            suggested_suspect = frontendname_dict.get(prev_game_state['suggested_cards']['character'])
            frontend_tile = tilename_dict.get(prev_game_state['suggested_cards']['room'])
            self.move_token(suggested_suspect, self.tiles_directory[frontend_tile][1])

            self.board.display_update(self.screen, f"Success! Player {prev_game_state['player_id']} has suggested {prev_game_state['suggested_cards']['character']} used the {prev_game_state['suggested_cards']['weapon']} in the {prev_game_state['suggested_cards']['room']}!", (400,30))
            # pygame.time.delay(500)
            
            if this_player_id == self.player_id:
                if 'suggest_result_player' in prev_game_state and prev_game_state['suggested_match_card'] != "No matched card found!":
                    print(prev_game_state['suggest_result_player'], "has shown you:", prev_game_state['suggested_match_card'])
                    self.board.display_update(self.screen, f"{prev_game_state['suggest_result_player']} has shown you: {prev_game_state['suggested_match_card']}", (400,30))
                    #pygame.time.wait(5000)
                else:
                    self.board.display_update(self.screen, f"No match found amongst other hands!", (400,30))
                    print("No match found amongst other hands!")
                    #pygame.time.wait(5000)
            else: 
                if 'suggest_result_player' in prev_game_state and prev_game_state['suggested_match_card'] != "No matched card found!":
                    print(f"{prev_game_state['suggest_result_player']} is showing Player {prev_game_state['player_id']} a card! How intriguing :)")
                    self.board.display_update(self.screen, f"{prev_game_state['suggest_result_player']} is showing Player {prev_game_state['player_id']} a card! How intriguing :)", (400,30))
                    #pygame.time.wait(5000)
                else:
                    self.board.display_update(self.screen, f"No match found amongst other hands!", (400,30))
                    print("No match found amongst other hands!")
            
            # pygame.time.delay(500)
            self.state = 'START'
            turn_data = self.network.build_client_package(self.player_id, self.state, '', '','') # 'next_player': '', 'next_playername_turn':''
            self.network.send(turn_data)
    
    ################################################################################
    # add_win_view is the function to show win view
    # Input : winner [type: Boolean], winner_player_id [type: int],  case_file [type: dict]
    ################################################################################    
    def add_win_screen(self, winner, winner_player_id, case_file):
        # Extract character, weapon, and room from case file
        readable_character = Client_message_handler.get_readable_playername(case_file['character'])
        readable_weapon = Client_message_handler.get_readable_weaponname(case_file['weapon'])
        readable_room = Client_message_handler.get_readable_tilename(case_file['room'])
        
        # mouse_pos = pygame.mouse.get_pos()
        image = pygame.image.load(data_folder / "splash.png")
        image = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
        self.screen.blit(image, (0, 0))

        TITLE_TEXT = self.get_font(65).render("CLUE-LESS", True, "#b68f40")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(530, 100))
        self.screen.blit(TITLE_TEXT, TITLE_RECT)
                    
      
    ################################################################################
    # add_win_view is the function to show win view
    # Input : winner [type: Boolean], winner_player_id [type: int],  case_file [type: dict]
    ################################################################################    
    def add_win_screen(self, winner, winner_player_id, case_file):
        # Extract character, weapon, and room from case file
        readable_character = Client_message_handler.get_readable_playername(case_file['character'])
        readable_weapon = Client_message_handler.get_readable_weaponname(case_file['weapon'])
        readable_room = Client_message_handler.get_readable_tilename(case_file['room'])
        
        # mouse_pos = pygame.mouse.get_pos()
        image = pygame.image.load(data_folder / "splash.png")
        image = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
        self.screen.blit(image, (0, 0))

        TITLE_TEXT = self.get_font(65).render("CLUE-LESS", True, "#b68f40")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(530, 100))
        self.screen.blit(TITLE_TEXT, TITLE_RECT)

        # Update win message for different clients
        MSG_TEXT = self.get_font(20).render(f'Sorry, Player {winner_player_id} won.', True, "#b68f40")
        if winner:
            MSG_TEXT = self.get_font(20).render('Congrats! You Win!!', True, "#b68f40")  
        MSG_RECT = MSG_TEXT.get_rect(center=(530, 300))
        self.screen.blit(MSG_TEXT, MSG_RECT)
        
        # Blit case file answer to all clients
        CASEFILE_TEXT =  self.get_font(20).render(f"Secret file was {readable_character}", True, "#b68f40")
        CASEFILE_RECT = CASEFILE_TEXT.get_rect(center=(530, 500))
        self.screen.blit(CASEFILE_TEXT, CASEFILE_RECT)
        
        CASEFILE_TEXT_REST =  self.get_font(20).render(f"with the {readable_weapon} in the {readable_room} ", True, "#b68f40")
        CASEFILE_RECT_REST = CASEFILE_TEXT_REST.get_rect(center=(530, 600))
        self.screen.blit(CASEFILE_TEXT_REST, CASEFILE_RECT_REST)
         
    def get_font(self,size): # Returns Press-Start-2P in the desired size
        font_folder = Path("clueless/data/font/")
        return pygame.font.Font(font_folder / "font.ttf", size)
    
    def add_splash_screen(self, events):
        mouse_pos = pygame.mouse.get_pos()
        image = pygame.image.load(data_folder / "splash.png")
        image = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
        self.screen.blit(image, (0, 0))

        TITLE_TEXT = self.get_font(65).render("CLUE-LESS", True, "#b68f40")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(530, 100))
        self.screen.blit(TITLE_TEXT, TITLE_RECT)

        PLAY_BUTTON = Splash_Button(image=pygame.image.load(data_folder / "Button_Image.png"), pos=(300, 450), 
                            text_input="PLAY", font=self.get_font(30), base_color="#76EEC6", hovering_color="White")
        QUIT_BUTTON = Splash_Button(image=pygame.image.load(data_folder / "Button_Image.png"), pos=(750, 450), 
                            text_input="QUIT", font=self.get_font(30), base_color="#76EEC6", hovering_color="White")


        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(mouse_pos)
            button.update(self.screen)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos):
                    self.state = 'CHOOSING_TOKEN'
                if QUIT_BUTTON.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

    def choose_player_token(self, events):
        self.screen.fill(self.base_color)
        mouse_pos = pygame.mouse.get_pos()

        # Load view from board class
        rectangle_dict = self.board.load_character_selection_board(self.screen)

        for event in events:
            if self.player_token == "None":
                for rect in rectangle_dict:
                    if (rectangle_dict[rect].collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN):
                        self.highlighted_character_rect = rectangle_dict[rect]
                        pygame.draw.rect(self.screen,"Red",rectangle_dict[rect],4)
                        print("Player " + self.player_id + ' choose ' + rect)

                        # send to server for player's token selection
                        self.player_token = rect
                        self.game_state['player_id'] = self.player_id
                        self.game_state['player_token'] = self.player_token
                        self.game_state['turn_status'] = "get"
                        game_data = self.network.build_client_package(self.player_id, "chose_token", self.player_token, '','') # 'next_player': '', 'next_playername_turn':''
                        self.network.send(game_data)

                        self.state = 'START'

        #token = "None"
        # print("Please choose your character token")
        # print(CHARACTER_TOKENS)
        # token = input("Please enter you character choice: ")
        # while token not in CHARACTER_TOKENS:
        #     token = input("Please enter a valid character choice: ")

        # print("You have chosen: " + token)
        
        #return "Professor Plum"
    def add_hands_view(self, hands_array):
        background = pygame.image.load(data_folder / "splash.png")
        background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
        self.screen.blit(background, (0, 0))

        translated_hands = []

        # TRANSLATE the hand array
        hand_dict = {'Study':'study',
                    'Hall':'hall',
                    'Lounge':'lounge',
                    'Library':'library',
                    'Billiard Room':'billiard',
                    'Dining Room':'dining',
                    'Conservatory':'conservatory',
                    'Ballroom':'ballroom',
                    'Kitchen':'kitchen',
                    'Rope':'rope',
                    'Lead Pipe':'leadpipe',
                    'Dagger':'dagger',
                    'Wrench':'wrench',
                    'Candlestick':'candlestick',
                    'Revolver':'revolver',
                    'Miss Scarlet':'miss_scarlet',
                    'Colonel Mustard':'colonel_mustard',
                    'Mrs. White':'mrs_white',
                    'Mr. Green':'mr_green',
                    'Mrs. Peacock':'mrs_peacock',
                    'Professor Plum':'prof_plum'}
        
        for each in hands_array:
            translated_hands.append(hand_dict[each])

        self.board.load_hands(self.screen, translated_hands)

        button_X_Pos = 440
        button_Y_Pos = 620
        button_color = (238,232,205)
        is_back_button_active = self.board.load_button(self.screen, "Back to Main", button_X_Pos, button_Y_Pos, button_color)

        if is_back_button_active:
            self.state = "START"
            self.screen.fill(self.base_color)

    def move_token(self,token_name, pos_tuple):
        # print("MOVING ")
        # print(token_name)
        # print(pos_tuple[0])
        # print(pos_tuple[1])
        self.token_coor_dict[token_name][1] = pos_tuple[0]
        self.token_coor_dict[token_name][2] = pos_tuple[1]


    def render(self):
        pygame.display.flip()
    
    def tick(self):
        self.clock.tick(self.FPS)

    def randomise_color(self):
        list_of_color = [(224,238,255), (203,204,255), (255,216,171), (255,234,253), (162,131,91), (110,137,215), (183,142,55), (234,231,240), (204,153,255), (126,135,145), (86,180,233),(213,94,0), (255,255,255), (75,0,146), (64,176,166)]
        return list_of_color[random.randint(0,len(list_of_color)-1)]
    
    def reset_weapon_and_suspect_dict(self, state):
        if (state == 'ACCUSATION'):
            for i in self.accuse_weapon_dict:
                    self.accuse_weapon_dict[i][3] = False
            for i in self.accuse_suspect_dict:
                    self.accuse_suspect_dict[i][3] = False
            for i in self.accuse_room_dict:
                    self.accuse_room_dict[i][3] = False

        if (state == 'SUGGESTION'):
            for i in self.suggest_weapon_dict:
                    self.suggest_weapon_dict[i][3] = False
            for i in self.suggest_suspect_dict:
                    self.suggest_suspect_dict[i][3] = False