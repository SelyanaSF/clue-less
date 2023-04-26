# Game Module
from sys import exit
from clueless.client.Client_message_handler import Client_message_handler
from clueless.server.Deck import Deck
from clueless.client.Weapon_image import Weapon_Image
from clueless.client import Button, Client_game_board
import pickle
import pygame
import random

from datetime import datetime
import time
import traceback

DEFAULT_GAME = dict({'player_id': '0', 'turn_status': 'get'})
server_update = dict({})

class Game_controller:

    # WIDTH AND HEIGHT OF THE WINDOW
    WIDTH = 1050
    HEIGHT = 700
    FPS = 60

    # There are FOUR Game State : "START", "MOVEMENT", "ACCUSATION", "SUGGESTION"
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
        self.state = "START"
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.base_color = self.randomise_color()
        self.screen.fill(self.base_color)
        self.clock = pygame.time.Clock()
        self.board = Client_game_board.Client_game_board()
        self.message_for_server = {}
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

        game_data = self.network.build_client_package(self.player_id, "get", '')

        while self.playing:
            self.tick()
            self.render()

            try:
                #game_update = self.network.get_server_update()
                current_time = datetime.now() 
                # print("....current Time =", current_time)
                
                # game = self.network.send_receive(game_data)
                # print("...sent and received client message")
                
                self.network.send(game_data)
                # print("...sent client message")

                try:
                    game = self.network.receive()
                except:
                    print("Couldn't receive server update")
                    break
                # game = self.network.receive()
                # print(f'......{game} ')
                # print(f'......{game_data} ')      
                                                      
                try:
                    prev_game_state = self.network.process_server_update(game, prev_game_state)
                    # print(f'server update: {prev_game_state} ')   
                    # TO DO read prev_game_state and display messages to corresponding players
                    if prev_game_state['turn_status']=='accusation':
                        this_player_id = prev_game_state['player_id']
                        if 'accused_result_player' not in prev_game_state:
                            print("You lost!")
                            self.board.display_update(self.screen, "You lost!")
                            # ISSUE: how to access other player id
                        else: 
                            print("You win!")
                    # elif  # print move stuff here
                except Exception as err:
                    print("Couldn't process_server_update")
                    print(err)
                    break

            except:
                run = False
                print("Couldn't get game")
                break

            events = pygame.event.get()
            game_data = self.check_events(events)
            # print(f'game_data is now {game_data}')
            # print()
            
        # when pygame.QUIT event happens, change self.playing to False 
        # the while loop will end and quit the game
        pygame.quit()

    ################################################################################
    # check_events is the function to check user's mouse movement
    # Input : events [type: Pygame Event]
    ################################################################################
    def check_events(self, events) :
        # print('...checking events')
        mousePos = pygame.mouse.get_pos()
        turn_data = DEFAULT_GAME
        for event in events:
            if event.type == pygame.QUIT:
                self.playing = False

            if (self.state == 'START'):
                self.message_for_server = {}
                self.room_choice = None
                self.screen.fill(self.base_color)
                turn_data = self.add_main_view(events)

            # This is to highlight rectangle when choosing the room and print the choosen one on the options box
            if (self.state == 'MOVING'): #'MOVEMENT'):
                turn_data = self.add_main_view(events)
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
                        # print('Player choose to go to tile : ' + self.room_choice)
                        self.message_for_server["room"] = self.room_choice
                        # print('Updated self.message_for_server with room choice')
                        # self.state = "START"
                        self.state = "MOVEMENT"
                        # SEND MESSAGE TO SERVER
                        turn_data = self.network.build_client_package(self.player_id, self.state, self.room_choice)
                        # self.network.send(turn_data)
                        # print(f"sending message to server for movement: {self.player_id}, {self.state}, {self.room_choice}")

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
                            self.message_for_server['weapon'] = key
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
                            self.message_for_server['suspect'] = key
                            self.character_choice = key

                turn_data = self.network.build_client_package(self.player_id, self.state, suggested_card_dict)

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
                            self.message_for_server['weapon'] = key
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
                            self.message_for_server['suspect'] = key
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
                            self.message_for_server['room'] = key
                            self.room_choice = key
                # # Testing receive here
                # turn_data = self.network.receive()
                # print(f"receiving message from server after accusation: {turn_data}")
                turn_data = self.network.build_client_package(self.player_id, self.state, accused_card_dict)

        return turn_data

    ################################################################################
    # add_main_view is the function to show main view
    # Input : events [type: Pygame Event]
    ################################################################################
    def add_main_view(self, events):

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
        self.board.load_player_tokens(self.screen, self.board)

        mousePos = pygame.mouse.get_pos()
        if is_Room_Selection_Active:
            # self.state = "MOVEMENT"
            self.state = "MOVING"
            self.board.load_options(self.screen, self.state, events)
            # print('Player chose to move')
            # This data stores the mouse position of the button
            turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos))
            self.network.send(turn_data)

        if is_Accuse_Selection_Active:
            # self.state = "ACCUSATION"
            self.state = "ACCUSING"
            self.board.load_options(self.screen, self.state, events)
            turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos))
            #print(turn_data)
            self.network.send(turn_data)

        if is_Suggest_Selection_Active:
            self.state = "SUGGESTING"
            self.board.load_options(self.screen, self.state, events)
            turn_data = self.network.build_client_package(self.player_id, self.state, str(mousePos))
            #print(turn_data)
            self.network.send(turn_data)

        # if player chooose end turn, then it passes the turn to others.

        return turn_data

    ################################################################################
    # add_suggest_view is the function to show suggest view
    # Input : events [type: Pygame Event]
    ################################################################################
    def add_suggest_view(self, events):
        suggested_card_dict = {}
        mousePos = pygame.mouse.get_pos()
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
            # print(self.message_for_server)

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
        mousePos = pygame.mouse.get_pos()
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
            
    def render(self):
        pygame.display.flip()
    
    def tick(self):
        self.clock.tick(self.FPS)

    def randomise_color(self):
        list_of_color = [(224,238,255), (203,204,255), (255,216,171), (255,234,253), (162,131,91), (110,137,215), (183,142,55), (234,231,240), (204,153,255), (126,135,145), (86,180,233), (0,0,0),(213,94,0), (255,255,255), (75,0,146), (64,176,166)]
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
