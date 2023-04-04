# Game Module
from sys import exit
from clueless import Board, Button, Network
from clueless.Network import Network
import pickle
import pygame
import random

DEFAULT_GAME = dict({'player_count': 0, 'player_turn_id': '0', 'player_turn_type': '', 'player_turn_details': ''})

class Game:
    WIDTH = 875
    HEIGHT = 700
    FPS = 60

    def __init__(self):
        pygame.init()
        
        self.network = Network()
        self.id = int(self.network.get_id())
        self.playing = True
        player_caption = "Clue-Less Player " + str(self.id)
        pygame.display.set_caption(player_caption)
        self.state = "START"
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.base_color = self.randomise_color()
        self.screen.fill(self.base_color)
        self.clock = pygame.time.Clock()
        self.gameLoop()

    def gameLoop(self):

        prev_game_state = DEFAULT_GAME
        print("You are Player ", self.id)

        while self.playing:
            self.tick()
            self.render()

            try:
                game_data = self.network.build_package("get", "")
                #print(game_data)
                game = self.network.send_receive(game_data)

                #receive updates
                if game != prev_game_state:
                    #print(game)
                    game_player_id = game['player_turn_id']
                    game_player_status = game['player_turn_type']
                    game_player_turn = game['player_turn_details']

                    if game_player_status == 'CHOOSING':
                        print("Player taking turn: Player ", game_player_id)
                        print("Player chooses to move to location ", game_player_turn)
                        print()

                    prev_game_state = game

            except:
                run = False
                print("Couldn't get game")
                break

            events = pygame.event.get()
            self.checkEvents(events)
            self.addView()
            
        # when pygame.QUIT event happens, change self.playing to False 
        # the while loop will end and quit the game
        pygame.quit()

    def checkEvents(self, events) :
        for event in events:
            if event.type == pygame.QUIT:
                self.playing = False

    def addView(self):
        # Add board
        board = Board.Board()
        board.loadTiles(self.screen, board)

        # Initialize Buttons
        buttonYPos = 75
        buttonXPos = 650
        buttonDistance = 60
        isRoomSelectionActive = board.loadButton(self.screen, "Go To Room", buttonXPos, buttonYPos)
        isAccuseSelectionActive = board.loadButton(self.screen, "Accuse", buttonXPos, buttonYPos + buttonDistance)
        isSuggestSelectionActive = board.loadButton(self.screen, "Suggest", buttonXPos, buttonYPos + buttonDistance*2)
        isEndTurnSelectionActive = board.loadButton(self.screen, "End Turn", buttonXPos, buttonYPos + buttonDistance*3)
        
        # Initialize valid players 
        # TO DO: players should be added to screen later depending on which tokens are chosen (here for now to test)
        board.load_player_tokens(self.screen, board)

        mousePos = pygame.mouse.get_pos()
        if isRoomSelectionActive:
            self.state = "CHOOSING"
            board.loadRoomOptions(self.screen)
            turn_data = self.network.build_package(self.state, str(mousePos))
            #print(turn_data)
            self.network.send(turn_data)

        #Manually record the rectangle position of close button. Everytime this button is pressed, close the options box
        closeRect = pygame.Rect(820, 570, 55, 30)
        if (closeRect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1 and self.state == 'CHOOSING'):
            board.closeRoomOptions(self.screen, self.base_color)
            self.state = "START"
            isRoomSelectionActive = False

    def render(self):
        pygame.display.update()

    def tick(self):
        self.clock.tick(self.FPS)

    def randomise_color(self):
        list_of_color = [(224,238,255), (203,204,255), (255,216,171), (255,234,253), (162,131,91), (110,137,215), (183,142,55), (234,231,240), (204,153,255), (126,135,145), (86,180,233), (0,0,0),(213,94,0), (255,255,255), (75,0,146), (64,176,166)]
        return list_of_color[random.randint(0,len(list_of_color)-1)]
