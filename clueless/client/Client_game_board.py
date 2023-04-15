# Board Module
import pygame
from clueless.client import Options_Box, Token
from pathlib import Path

from clueless.client import Button

data_folder = Path("clueless/data/graphics/")

class Client_game_board:
    WIDTH = 550
    HEIGHT = 550
    board_Y_Pos = 75
    board_X_Pos = 75
    # buttonYPos = 75
    # buttonXPos = 650
    
    def __init__(self):
        self.board_surface = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.board_surface.fill('bisque3')

        self.study_room_surface = pygame.image.load(data_folder / 'study.png').convert_alpha()
        self.study_room_surface = pygame.transform.scale(self.study_room_surface, (140, 170))
        self.study_room_rect = self.study_room_surface.get_rect()

        self.hall_surface = pygame.image.load(data_folder / 'hall.png').convert_alpha()
        self.hall_surface = pygame.transform.scale(self.hall_surface, (130, 135))
        self.hall_rect = self.hall_surface.get_rect()

        self.lounge_surface = pygame.image.load(data_folder / 'lounge.png').convert_alpha()
        self.lounge_surface = pygame.transform.scale(self.lounge_surface, (130, 150))
        self.lounge_rect = self.lounge_surface.get_rect()

        self.library_surface = pygame.image.load(data_folder / 'library.png').convert_alpha()
        self.library_surface = pygame.transform.scale(self.library_surface, (135, 125))
        self.library_rect = self.library_surface.get_rect()

        self.billiard_room_surface = pygame.image.load(data_folder / 'billiard.png').convert_alpha()
        self.billiard_room_surface = pygame.transform.scale(self.billiard_room_surface, (150, 130))
        self.billiard_room_rect = self.billiard_room_surface.get_rect()

        self.dining_room_surface = pygame.image.load(data_folder / 'dining.png').convert_alpha()
        self.dining_room_surface = pygame.transform.scale(self.dining_room_surface, (145, 130))
        self.dining_room_rect = self.dining_room_surface.get_rect()

        self.conservatory_surface = pygame.image.load(data_folder / 'conservatory.png').convert_alpha()
        self.conservatory_surface = pygame.transform.scale(self.conservatory_surface, (125, 140))
        self.conservatory_rect = self.conservatory_surface.get_rect()

        self.ballroom_surface = pygame.image.load(data_folder / 'ballroom.png').convert_alpha()
        self.ballroom_surface = pygame.transform.scale(self.ballroom_surface, (140, 135))
        self.ballroom_rect = self.ballroom_surface.get_rect()

        self.kitchen_surface = pygame.image.load(data_folder / 'kitchen.png').convert_alpha()
        self.kitchen_surface = pygame.transform.scale(self.kitchen_surface, (130, 130))
        self.kitchen_rect = self.kitchen_surface.get_rect()

        self.hallway = pygame.image.load(data_folder / 'hallway.PNG').convert_alpha()
        self.hallway = pygame.transform.scale(self.hallway, (100, 45))
        self.hallway_rect = self.hallway.get_rect()

        self.hallwayVertical = pygame.transform.scale(self.hallway, (50, 100))
        self.hallwayVertical_rect = self.hallwayVertical.get_rect()
        
    
    def load_tiles(self, screen, board):
        screen.blit(board.board_surface,(self.board_X_Pos,self.board_Y_Pos))
        # Initialize hallways
        screen.blit(board.hallwayVertical,(125,200))
        screen.blit(board.hallwayVertical,(325,200))
        screen.blit(board.hallwayVertical,(525,200))
        screen.blit(board.hallwayVertical,(125,400))
        screen.blit(board.hallwayVertical,(325,400))
        screen.blit(board.hallwayVertical,(525,400))

        screen.blit(board.hallway,(200,125))
        screen.blit(board.hallway,(400,125))
        screen.blit(board.hallway,(200,325))
        screen.blit(board.hallway,(400,325))
        screen.blit(board.hallway,(200,525))
        screen.blit(board.hallway,(400,525))

        screen.blit(board.study_room_surface,(100,80))
        screen.blit(board.lounge_surface,(480,100))
        screen.blit(board.conservatory_surface,(100,480))
        screen.blit(board.kitchen_surface,(480,480))

        screen.blit(board.hall_surface,(290,100))
        screen.blit(board.library_surface,(90,300))
        screen.blit(board.dining_room_surface,(480,300))
        screen.blit(board.ballroom_surface,(285,480))
        screen.blit(board.billiard_room_surface,(280,290))

    def load_player_tokens(self, screen, board):
        chosen_tokens = ['Professor Plum', 'Colonel Mustard','Miss Scarlet', 'Mr Green', 'Mrs White', 'Mrs Peacock'] # input param
        
        # Dictionary stores each token image file name, x location, and y location on the board
        token_info_dict = {'Professor Plum':['prof_plum', 60, 210],
                           'Mrs Peacock':['mrs_peacock', 60, 410],
                           'Mr Green':['mr_green', 210, 550],
                           'Mrs White':['mrs_white', 410, 550],
                           'Miss Scarlet':['miss_scarlet', 410, 60],
                           'Colonel Mustard':['colonel_mustard', 560, 210]}
         
        # Initialize token positions for chosen tokens
        for token in chosen_tokens:
            token_surface = pygame.Surface((100, 100))
            token_image = pygame.image.load(f'{data_folder / token_info_dict[token][0]}.PNG').convert_alpha()
            token_image = pygame.transform.scale(token_image, (80, 80))
            
            pygame.draw.rect(token_image, 'BLACK', pygame.Rect(0, 0, 100, 100), 1)
            token_rect = (token_info_dict[token][1], token_info_dict[token][2], 100, 100)
            screen.blit(token_image, token_rect) 
            
    
    def load_button(self, screen, text, buttonXPos, buttonYPos):
        button_color = (150, 150, 150)
        button_width = 160
        button_height = 40
        button_highlight_color = (100, 200, 255)
        button_font = pygame.font.SysFont(None, 30)

        goToRoom_button = Button.Button(buttonXPos, buttonYPos, button_width, button_height, button_color, button_highlight_color, button_font, text)
        goToRoom_button.draw(screen)
        return goToRoom_button.draw(screen)

    def load_options(self, screen, state, events):

        room_options = Options_Box.OptionsBox()
        if (state == "CHOOSING_ROOM"):
            return room_options.draw_room_options(screen)
        elif (state == "ACCUSING"):
            return room_options.draw_accuse_options(screen, events)
        elif (state == "SUGGESTING"):
            return room_options.draw_suggest_options(screen)
        else :
            print("No options box drawed")
    
    def close_room_options(self, screen, color):

        room_options = Options_Box.OptionsBox()
        room_options.close_option(screen, color)

    def display_update(self, screen, board, update_text):        
        pygame.font.init() 
        my_font = pygame.font.SysFont(None, 30)
        text_surface = my_font.render(update_text, False, (0, 0, 0))
        screen.blit(text_surface, (650, 300))