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

class Game_controller:

    # WIDTH AND HEIGHT OF THE WINDOW
    WIDTH = 1050
    HEIGHT = 700
    FPS = 60

    # There are FOUR Game State : "START", "MOVING", "ACCUSING", "SUGGESTING", "CHOOSING_TOKEN", "SPLASH_SCREEN", "chose_token"
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
                    # print(f'prev_game_state is now {prev_game_state}')
                        
                    if (prev_game_state['player_id'] == self.player_id) and prev_game_state['turn_status'] == 'MOVING' and 'valid_tile_names_for_player' in prev_game_state:
                        while input_tile_name not in prev_game_state.get('valid_tile_names_for_player'):
                           input_tile_name = input("Please input a room from the list above: \n    ")
                        
                        print("    Success! Sending room selection to server...")

                        # update game data
                        game_data = self.network.build_client_package(self.player_id, 'MOVEMENT', input_tile_name, '','') # 'next_player': '', 'next_playername_turn':'')

                        # KT: take out this continue when ui is integrated, may cause 
                        # errors when you do but needed for command line input rn since
                        # it stops game_data from being overwritten at the end of the loop
                        continue
                    
                    else:
                        try: 
                            # Only update views after a move, suggest, or accuse
                            self.update_views(prev_game_state)
                        except Exception as err:
                            print(err) 
                         
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
                self.choose_player_token()
            
            if (self.state == 'MOVING'): #'MOVEMENT'):
                # print("check_events moving")
                turn_data = self.add_main_view(events, prev_game_state)
                self.board.highlight_tile_rect(self.screen,(0,100,0),'All')
                for key in self.tiles_directory:
                    if (self.tiles_directory[key][0].collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
                        pygame.draw.rect(self.screen, (202, 228, 241), (800,450,180,50), width=0, border_radius=5)
                        self.board.highlight_tile_rect(self.screen,(0,200,0),key)
                        message_font = pygame.font.SysFont('Comic Sans MS', 14)
                        message_surface = message_font.render( key + '.  Proceed?', False, (120,39,64))
                        message_surface_rect = message_surface.get_rect(topleft = (810, 450))
                        self.screen.blit(message_surface, message_surface_rect)
                        self.room_choice = key

                enterRect = pygame.Rect(810, 560, 60, 35)
                if (enterRect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
                    if self.room_choice is not None:
                        self.state = "MOVING"
                        # SEND MESSAGE TO SERVER AND MOVE TOKEN
                        turn_data = self.network.build_client_package(self.player_id, self.state, self.room_choice, '','') # 'next_player': '', 'next_playername_turn':''
                        self.move_token(self.player_token, self.tiles_directory[self.room_choice][1])
                        # self.network.send(turn_data)
                        print(turn_data)
                        # print(f"sending message to server for movement: {self.player_id}, {self.state}, {self.room_choice}")
                        self.state = 'START'

                #Manually record the rectangle position of close button. Everytime this button is pressed, close the options box
                closeRect = pygame.Rect(970, 570, 25, 25)
                if (closeRect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
                    self.board.close_room_options(self.screen, self.base_color)
                    self.state = "START"
                    #is_Room_Selection_Active = False

            if (self.state == 'SUGGESTING'):
                suggested_card_dict = self.add_suggest_view(events)

                for key in self.suggest_weapon_dict:
                    if self.suggest_weapon_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.suggest_weapon_dict[key][2],key)
                    if (self.suggest_weapon_dict[key][0].collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
                        for i in self.suggest_weapon_dict:
                            self.suggest_weapon_dict[i][3] = False
                        if (self.suggest_weapon_dict[key][2] == 'weapon') :
                            # print('Player choose weapon: ' + key)
                            self.suggest_weapon_dict[key][3] = True
                            self.weapon_choice = key

                for key in self.suggest_suspect_dict:
                    if self.suggest_suspect_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.suggest_suspect_dict[key][2],key)
                    if (self.suggest_suspect_dict[key][0].collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
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
                    if (self.accuse_weapon_dict[key][0].collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
                        for i in self.accuse_weapon_dict:
                            self.accuse_weapon_dict[i][3] = False
                        if (self.accuse_weapon_dict[key][2] == 'weapon') :
                            # print('Player choose weapon: ' + key)
                            self.accuse_weapon_dict[key][3] = True
                            self.weapon_choice = key

                for key in self.accuse_suspect_dict:
                    if self.accuse_suspect_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.accuse_suspect_dict[key][2],key)
                    if (self.accuse_suspect_dict[key][0].collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
                        for i in self.accuse_suspect_dict:
                            self.accuse_suspect_dict[i][3] = False
                        if (self.accuse_suspect_dict[key][2] == 'suspect') :
                            # print('Player choose suspect: ' + key)
                            self.accuse_suspect_dict[key][3] = True
                            self.character_choice = key

                for key in self.accuse_room_dict:
                    if self.accuse_room_dict[key][3] == True:
                        self.board.highlight_rect(self.screen,(0,200,0),self.accuse_room_dict[key][2],key)
                    if (self.accuse_room_dict[key][0].collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1):
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
                    
            # HERE is this needed?
            # if (self.state == 'END TURN'):
            #     turn_dict = {'':''}
            #     turn_data = self.network.build_client_package(self.player_id, self.state, turn_dict)
            #     print(f'... turn data is now {turn_data}')
                
        return turn_data

    ################################################################################
    # add_main_view is the function to show main view
    # Input : events [type: Pygame Event]
    ################################################################################
    def add_main_view(self, events, prev_game_state):        
        player_caption = "Clue-Less Player " + str(self.id)
        pygame.display.set_caption(player_caption)
        # Add board
        self.board.load_tiles(self.screen, self.board)
        self.tiles_directory = self.board.get_tiles_directory()
        turn_data = DEFAULT_GAME

        # Initialize Buttons
        button_Y_Pos = 75
        button_X_Pos = 800
        button_distance = 60
        is_Room_Selection_Active = self.board.load_button(self.screen, "Go To Room", button_X_Pos, button_Y_Pos)
        is_Suggest_Selection_Active = self.board.load_button(self.screen, "Suggest", button_X_Pos, button_Y_Pos + button_distance)
        is_Accuse_Selection_Active = self.board.load_button(self.screen, "Accuse", button_X_Pos, button_Y_Pos + button_distance*2)
        isEndTurnSelectionActive = self.board.load_button(self.screen, "End Turn", button_X_Pos, button_Y_Pos + button_distance*3)
        
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

        # if player chooose end turn, then it passes the turn to others.
        if isEndTurnSelectionActive:
            self.state = "END TURN"
            # self.board.load_options(self.screen, self.state, events)
            turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos), '','') # 'next_player': '', 'next_playername_turn':''
            # #print(turn_data)
            self.network.send(turn_data)

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
        is_back_button_active = self.board.load_button(self.screen, "Back to Main", button_X_Pos, button_Y_Pos)
        is_submit_button_active = self.board.load_button(self.screen, "Submit", button_X_Pos+350, button_Y_Pos)

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
        is_back_button_active = self.board.load_button(self.screen, "Back to Main", button_X_Pos, button_Y_Pos)
        is_submit_button_active = self.board.load_button(self.screen, "Submit", button_X_Pos+350, button_Y_Pos)

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
                # TO FINALIZE
                if this_player_id == self.player_id:
                    print("You Lost!")
                    self.board.display_update(self.screen, "Sorry, You Lost!", (300, 30))
                else:
                    print(f"Player {this_player_id} Lost!")
                    self.board.display_update(self.screen, f"Player {this_player_id} Lost!", (300, 30))
                    
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
        elif (prev_game_state['player_id'] == self.player_id) and prev_game_state['turn_status'] == 'suggestion' and 'suggested_cards' in prev_game_state:
            print(f"Success! Player {prev_game_state['player_id']} (you) have suggested {prev_game_state['suggested_cards']}!")
            if this_player_id == self.player_id:
                if 'suggest_result_player' in prev_game_state and prev_game_state['suggested_match_card'] != "No matched card found!":
                    print(prev_game_state['suggest_result_player'], "has shown you:", prev_game_state['suggested_match_card'])
                    self.board.display_update(self.screen, f"{prev_game_state['suggest_result_player']} has shown you: {prev_game_state['suggested_match_card']}", (400, 400))
                else:
                    self.board.display_update(self.screen, f"No match found amongst other hands!", (400, 400))
                    print("No match found amongst other hands!")
                    
        # ALL CHOSE TOKEN finished, starting game
        elif prev_game_state['turn_status'] == 'start game' :
            first_player_id = prev_game_state['next_player']
            print(prev_game_state)
            # Player's first turn
            if first_player_id == self.player_id:
                print("It's your first turn")
                self.board.display_update(self.screen, f"It's your first turn", (300, 30))
            # Other players, not their turn
            else:
                print(f"It's {prev_game_state['next_playername_turn']}'s turn")
                self.board.display_update(self.screen, f"It's {prev_game_state['next_playername_turn']}'s turn", (300, 30))
        
        # END TURN finished
        elif prev_game_state['turn_status'] == 'end turn':
            # Player's turn just ended
            if this_player_id == self.player_id:
                self.board.display_update(self.screen, f"Your turn has ended", (300, 30))
                self.board.display_update(self.screen, f"It's {prev_game_state['next_playername_turn']}'s turn", (300, 50))
            # This player's turn
            elif prev_game_state['next_player'] == self.player_id:
                self.board.display_update(self.screen, f"It's your turn", (300, 30))
            # Other players, not their turn
            else:
                self.board.display_update(self.screen, f"It's {prev_game_state['next_playername_turn']}'s turn", (300, 30))
    
    ################################################################################
    # add_win_view is the function to show win view
    # Input : winner [type: Boolean], winner_player_id [type: int],  case_file [type: dict]
    ################################################################################    
    def add_win_screen(self, winner, winner_player_id, case_file):
        # Extract character, weapon, and room from case file
        readable_character = Client_message_handler.get_readable_playername(case_file['character'])
        readable_weapon = Client_message_handler.get_readable_weaponname(case_file['weapon'])
        readable_room = Client_message_handler.get_readable_tilename(case_file['room'])
        
        data_folder = Path("clueless/data/graphics/")
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
        data_folder = Path("clueless/data/font/")
        return pygame.font.Font(data_folder / "font.ttf", size)
    
    def add_splash_screen(self, events):
        data_folder = Path("clueless/data/graphics/")
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

    def choose_player_token(self):
        # token = "None"
        # print("Please choose your character token")
        # print(CHARACTER_TOKENS)
        # token = input("Please enter your character choice: ")
        #while token not in CHARACTER_TOKENS:
        #    token = input("Please enter a valid character choice: ")

        # print("You have chosen: " + token)
        self.screen.fill(self.base_color)
        mouse_pos = pygame.mouse.get_pos()

        # Load view from board class
        rectangle_dict = self.board.load_character_selection_board(self.screen)
        
        if self.player_token == "None":
            for rect in rectangle_dict:
                if (rectangle_dict[rect].collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1):
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
################################################################################
# Instantiate Deck class
# Remove docstring to execute 

# players= []

# num_players= int(input("Enter the number of players: "))

# assert 6 >= num_players >=3, f"A total number of 3-6 players are allowed to\
#  participate in this game."
################################################################################

#Instatiate Weapon_Image Class 
# Remove docstring to execute 
'''
weapon_dict= {
    'Dagger':'dagger.png', 'Candlestick':'candlestick.png', 'Wrench': 'wrench.png',
    'Leadpipe':'leadpipe.png', 'Revolver': 'revolver.png', 'Rope': 'rope.png'
}

wep_img= Weapon_Image()

# Enter the name of your Weapon
weapon_name= input("State the name of your Weapon (first letter capitalized) to display image: ")
wep_img.display_weapon_image(weapon_dict[weapon_name])
'''
################################################################################
