# Board Module
import pygame
from clueless.client import Options_Box, Token
from pathlib import Path

from clueless.client import Button

data_folder = Path("clueless/data/graphics/")

class Client_game_board:
    WIDTH = 700
    HEIGHT = 550
    board_Y_Pos = 75
    board_X_Pos = 75
    
    def __init__(self):
        self.board_surface = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.board_surface.fill('bisque3')
        self.tile_rect_dict = {}
        self.weapon_dict = {}
        self.suspect_dict = {}
        self.room_dict = {}

        self.study_room_surface = pygame.image.load(data_folder / 'study.png').convert_alpha()
        self.study_room_surface = pygame.transform.scale(self.study_room_surface, (140, 120))
        self.study_room_rect = self.study_room_surface.get_rect(topleft=(100,85))
        self.tile_rect_dict["study_room"] = [self.study_room_rect, (100,85)]

        self.study_room_surface_accuse = pygame.transform.scale(self.study_room_surface, (110, 90))
        self.study_room_rect_accuse = self.study_room_surface_accuse.get_rect(topleft=(35,440))
        self.room_dict["study_room"] = [self.study_room_rect_accuse, (35,440),"room",False]

        self.hall_surface = pygame.image.load(data_folder / 'hall.png').convert_alpha()
        self.hall_surface = pygame.transform.scale(self.hall_surface, (130, 135))
        self.hall_rect = self.hall_surface.get_rect(topleft=(290,90))
        self.tile_rect_dict["hall"] = [self.hall_rect, (290,90)]

        self.hall_surface_accuse = pygame.transform.scale(self.hall_surface, (100, 105))
        self.hall_rect_accuse = self.hall_surface_accuse.get_rect(topleft=(160,440))
        self.room_dict["hall"] = [self.hall_rect_accuse, (155,440),"room",False]

        self.lounge_surface = pygame.image.load(data_folder / 'lounge.png').convert_alpha()
        self.lounge_surface = pygame.transform.scale(self.lounge_surface, (120, 140))
        self.lounge_rect = self.lounge_surface.get_rect(topleft=(480,100))
        self.tile_rect_dict["lounge"] = [self.lounge_rect, (480,100)]

        self.lounge_surface_accuse = pygame.transform.scale(self.lounge_surface, (90, 110))
        self.lounge_rect_accuse = self.lounge_surface_accuse.get_rect(topleft=(260,440))
        self.room_dict["lounge"] = [self.lounge_rect_accuse, (260,440),"room",False]

        self.library_surface = pygame.image.load(data_folder / 'library.png').convert_alpha()
        self.library_surface = pygame.transform.scale(self.library_surface, (135, 125))
        self.library_rect = self.library_surface.get_rect(topleft=(90,300))
        self.tile_rect_dict["library"] = [self.library_rect, (90,300)]

        self.library_surface_accuse = pygame.transform.scale(self.library_surface, (95, 85))
        self.library_rect_accuse = self.library_surface_accuse.get_rect(topleft=(365,440))
        self.room_dict["library"] = [self.library_rect_accuse, (365,440),"room",False]

        self.billiard_room_surface = pygame.image.load(data_folder / 'billiard.png').convert_alpha()
        self.billiard_room_surface = pygame.transform.scale(self.billiard_room_surface, (140, 120))
        self.billiard_room_rect = self.billiard_room_surface.get_rect(topleft=(280,290))
        self.tile_rect_dict["billiard_room"] = [self.billiard_room_rect, (280,290)]

        self.billiard_room_surface_accuse = pygame.transform.scale(self.billiard_room_surface, (95, 95))
        self.billiard_room_rect_accuse = self.billiard_room_surface_accuse.get_rect(topleft=(470,440))
        self.room_dict["billiard_room"] = [self.billiard_room_rect_accuse, (470,440),"room",False]

        self.dining_room_surface = pygame.image.load(data_folder / 'dining.png').convert_alpha()
        self.dining_room_surface = pygame.transform.scale(self.dining_room_surface, (145, 140))
        self.dining_room_rect = self.dining_room_surface.get_rect(topleft=(480,300))
        self.tile_rect_dict["dining_room"] = [self.dining_room_rect,(480,300)]

        self.dining_room_surface_accuse = pygame.transform.scale(self.dining_room_surface, (105, 95))
        self.dining_room_rect_accuse = self.dining_room_surface_accuse.get_rect(topleft=(575,440))
        self.room_dict["dining_room"] = [self.dining_room_rect_accuse,(575,440),"room",False]

        self.conservatory_surface = pygame.image.load(data_folder / 'conservatory.png').convert_alpha()
        self.conservatory_surface = pygame.transform.scale(self.conservatory_surface, (125, 140))
        self.conservatory_rect = self.conservatory_surface.get_rect(topleft=(100,480))
        self.tile_rect_dict["conservatory"] = [self.conservatory_rect,(100,480)]

        self.conservatory_surface_accuse = pygame.transform.scale(self.conservatory_surface, (100, 115))
        self.conservatory_rect_accuse = self.conservatory_surface_accuse.get_rect(topleft=(690,440))
        self.room_dict["conservatory"] = [self.conservatory_rect_accuse,(690,440),"room",False]

        self.ballroom_surface = pygame.image.load(data_folder / 'ballroom.png').convert_alpha()
        self.ballroom_surface = pygame.transform.scale(self.ballroom_surface, (140, 135))
        self.ballroom_rect = self.ballroom_surface.get_rect(topleft=(285,480))
        self.tile_rect_dict["ballroom"] = [self.ballroom_rect,(285,480)]

        self.ballroom_surface_accuse = pygame.transform.scale(self.ballroom_surface ,(120, 115))
        self.ballroom_rect_accuse = self.ballroom_surface_accuse.get_rect(topleft=(800,440))
        self.room_dict["ballroom"] = [self.ballroom_rect_accuse,(800,440),"room",False]

        self.kitchen_surface = pygame.image.load(data_folder / 'kitchen.png').convert_alpha()
        self.kitchen_surface = pygame.transform.scale(self.kitchen_surface, (130, 130))
        self.kitchen_rect = self.kitchen_surface.get_rect(topleft=(480,480))
        self.tile_rect_dict["kitchen"] = [self.kitchen_rect,(480,480)]

        self.kitchen_surface_accuse = pygame.transform.scale(self.kitchen_surface ,(100, 95))
        self.kitchen_rect_accuse = self.kitchen_surface_accuse.get_rect(topleft=(925,440))
        self.room_dict["kitchen"] = [self.kitchen_rect_accuse,(925,440),"room",False]

        self.hallway_image = pygame.image.load(data_folder / 'hallway.PNG').convert_alpha()

        self.hallway_1 = pygame.transform.scale(self.hallway_image, (100, 45))
        self.hallway_1_rect = self.hallway_1.get_rect(topleft=(200,125))
        self.tile_rect_dict["hallway_1"] = [self.hallway_1_rect, (200,125)]

        self.hallway_2 = pygame.transform.scale(self.hallway_image, (100, 45))
        self.hallway_2_rect = self.hallway_2.get_rect(topleft=(400,125))
        self.tile_rect_dict["hallway_2"] = [self.hallway_2_rect, (400,125)]

        self.hallway_6 = pygame.transform.scale(self.hallway_image, (100, 45))
        self.hallway_6_rect = self.hallway_6.get_rect(topleft=(200,325))
        self.tile_rect_dict["hallway_6"] = [self.hallway_6_rect, (200,325)]

        self.hallway_7 = pygame.transform.scale(self.hallway_image, (100, 45))
        self.hallway_7_rect = self.hallway_7.get_rect(topleft=(400,325))
        self.tile_rect_dict["hallway_7"] = [self.hallway_7_rect,(400,325)]

        self.hallway_11 = pygame.transform.scale(self.hallway_image, (100, 45))
        self.hallway_11_rect = self.hallway_11.get_rect(topleft=(200,525))
        self.tile_rect_dict["hallway_11"] = [self.hallway_11_rect,(200,525)]

        self.hallway_12 = pygame.transform.scale(self.hallway_image, (100, 45))
        self.hallway_12_rect = self.hallway_12.get_rect(topleft=(400,525))
        self.tile_rect_dict["hallway_12"] = [self.hallway_12_rect,(400,525)]

        self.hallway_3 = pygame.transform.scale(self.hallway_image, (50, 100))
        self.hallway_3_rect = self.hallway_3.get_rect(topleft=(125,200))
        self.tile_rect_dict["hallway_3"] = [self.hallway_3_rect, (125,200)]

        self.hallway_4 = pygame.transform.scale(self.hallway_image, (50, 100))
        self.hallway_4_rect = self.hallway_4.get_rect(topleft=(325,200))
        self.tile_rect_dict["hallway_4"] = [self.hallway_4_rect, (325,200)]

        self.hallway_5 = pygame.transform.scale(self.hallway_image, (50, 100))
        self.hallway_5_rect = self.hallway_5.get_rect(topleft=(525,200))
        self.tile_rect_dict["hallway_5"] = [self.hallway_5_rect, (525,200)]

        self.hallway_8 = pygame.transform.scale(self.hallway_image, (50, 100))
        self.hallway_8_rect = self.hallway_8.get_rect(topleft=(125,400))
        self.tile_rect_dict["hallway_8"] = [self.hallway_8_rect, (125,400)]

        self.hallway_9 = pygame.transform.scale(self.hallway_image, (50, 100))
        self.hallway_9_rect = self.hallway_9.get_rect(topleft=(325,400))
        self.tile_rect_dict["hallway_9"] = [self.hallway_9_rect, (325,400)]

        self.hallway_10 = pygame.transform.scale(self.hallway_image, (50, 100))
        self.hallway_10_rect = self.hallway_10.get_rect(topleft=(525,400))
        self.tile_rect_dict["hallway_10"] = [self.hallway_10_rect, (525,400)]

        self.colonel_mustard = pygame.image.load(data_folder / 'colonel_mustard.png').convert_alpha()
        self.colonel_mustard = pygame.transform.scale(self.colonel_mustard, (100, 120))
        self.colonel_mustard_rect = self.colonel_mustard.get_rect(topleft=(70,85))
        self.suspect_dict["colonel_mustard"] = [self.colonel_mustard_rect, (70,85),"suspect",False]
        
        self.miss_scarlet = pygame.image.load(data_folder / 'miss_scarlet.png').convert_alpha()
        self.miss_scarlet = pygame.transform.scale(self.miss_scarlet, (100, 120))
        self.miss_scarlet_rect = self.miss_scarlet.get_rect(topleft=(230,85))
        self.suspect_dict["miss_scarlet"] = [self.miss_scarlet_rect,(230,85),"suspect",False]

        self.mr_green = pygame.image.load(data_folder / 'mr_green.png').convert_alpha()
        self.mr_green = pygame.transform.scale(self.mr_green, (100, 120))
        self.mr_green_rect = self.mr_green.get_rect(topleft=(390,85))
        self.suspect_dict["mr_green"] = [self.mr_green_rect, (390,85),"suspect",False]

        self.mrs_peacock = pygame.image.load(data_folder / 'mrs_peacock.png').convert_alpha()
        self.mrs_peacock = pygame.transform.scale(self.mrs_peacock, (100, 120))
        self.mrs_peacock_rect = self.mrs_peacock.get_rect(topleft=(550,85))
        self.suspect_dict["mrs_peacock"] = [self.mrs_peacock_rect, (550,85),"suspect",False]

        self.mrs_white = pygame.image.load(data_folder / 'mrs_white.png').convert_alpha()
        self.mrs_white = pygame.transform.scale(self.mrs_white, (100, 120))
        self.mrs_white_rect = self.mrs_white.get_rect(topleft=(710,85))
        self.suspect_dict["mrs_white"] = [self.mrs_white_rect, (710,85),"suspect",False]

        self.prof_plum = pygame.image.load(data_folder / 'prof_plum.png').convert_alpha()
        self.prof_plum = pygame.transform.scale(self.prof_plum, (100, 120))
        self.prof_plum_rect = self.prof_plum.get_rect(topleft=(870,85))
        self.suspect_dict["prof_plum"] = [self.prof_plum_rect, (870,85),"suspect",False]

        self.candlestick = pygame.image.load(data_folder / 'candlestick.png').convert_alpha()
        self.candlestick = pygame.transform.scale(self.candlestick, (140, 170))
        self.candlestick_rect = self.candlestick.get_rect(topleft=(60,250))
        self.weapon_dict["candlestick"] = [self.candlestick_rect, (60,250),"weapon",False]

        self.dagger = pygame.image.load(data_folder / 'dagger.png').convert_alpha()
        self.dagger = pygame.transform.scale(self.dagger, (140, 170))
        self.dagger_rect = self.dagger.get_rect(topleft=(220,250))
        self.weapon_dict["dagger"] = [self.dagger_rect, (220,250),"weapon",False]

        self.lead_pipe = pygame.image.load(data_folder / 'leadpipe.png').convert_alpha()
        self.lead_pipe = pygame.transform.scale(self.lead_pipe, (140, 170))
        self.lead_pipe_rect = self.lead_pipe.get_rect(topleft=(380,250))
        self.weapon_dict["lead_pipe"] = [self.lead_pipe_rect, (380,250),"weapon",False]
    
        self.revolver = pygame.image.load(data_folder / 'revolver.png').convert_alpha()
        self.revolver = pygame.transform.scale(self.revolver, (140, 170))
        self.revolver_rect = self.revolver.get_rect(topleft=(540,250))
        self.weapon_dict["revolver"] = [self.revolver_rect, (540,250),"weapon",False]

        self.rope = pygame.image.load(data_folder / 'rope.png').convert_alpha()
        self.rope = pygame.transform.scale(self.rope, (140, 170))
        self.rope_rect = self.rope.get_rect(topleft=(720,250))
        self.weapon_dict["rope"] = [self.rope_rect, (720,250),"weapon",False]

        self.wrench = pygame.image.load(data_folder / 'wrench.png').convert_alpha()
        self.wrench = pygame.transform.scale(self.wrench, (140, 170))
        self.wrench_rect = self.wrench.get_rect(topleft=(880,250))
        self.weapon_dict["wrench"] = [self.wrench_rect, (880,250),"weapon",False]
    
    def load_tiles(self, screen, board):
        screen.blit(board.board_surface,(self.board_X_Pos,self.board_Y_Pos))

        # Initialize hallways Vertical
        screen.blit(board.hallway_3,self.tile_rect_dict["hallway_3"][1])
        screen.blit(board.hallway_4,self.tile_rect_dict["hallway_4"][1])
        screen.blit(board.hallway_5,self.tile_rect_dict["hallway_5"][1])
        screen.blit(board.hallway_8,self.tile_rect_dict["hallway_8"][1])
        screen.blit(board.hallway_9,self.tile_rect_dict["hallway_9"][1])
        screen.blit(board.hallway_10,self.tile_rect_dict["hallway_10"][1])

        # Initialize hallways Horizontal
        screen.blit(board.hallway_1,self.tile_rect_dict["hallway_1"][1])
        screen.blit(board.hallway_2,self.tile_rect_dict["hallway_2"][1])
        screen.blit(board.hallway_6,self.tile_rect_dict["hallway_6"][1])
        screen.blit(board.hallway_7,self.tile_rect_dict["hallway_7"][1])
        screen.blit(board.hallway_11,self.tile_rect_dict["hallway_11"][1])
        screen.blit(board.hallway_12,self.tile_rect_dict["hallway_12"][1])
        
        # Initialize Rooms
        screen.blit(board.study_room_surface,self.tile_rect_dict["study_room"][1])
        screen.blit(board.lounge_surface,self.tile_rect_dict["lounge"][1])
        screen.blit(board.conservatory_surface,self.tile_rect_dict["conservatory"][1])
        screen.blit(board.kitchen_surface,self.tile_rect_dict["kitchen"][1])

        screen.blit(board.hall_surface,self.tile_rect_dict["hall"][1])
        screen.blit(board.library_surface,self.tile_rect_dict["library"][1])
        screen.blit(board.dining_room_surface,self.tile_rect_dict["dining_room"][1])
        screen.blit(board.ballroom_surface,self.tile_rect_dict["ballroom"][1])
        screen.blit(board.billiard_room_surface,self.tile_rect_dict["billiard_room"][1])

    def load_accuse_board(self, screen, board):
        screen.blit(board.colonel_mustard,self.suspect_dict["colonel_mustard"][1])
        screen.blit(board.miss_scarlet,self.suspect_dict["miss_scarlet"][1])
        screen.blit(board.mr_green,self.suspect_dict["mr_green"][1])
        screen.blit(board.mrs_peacock,self.suspect_dict["mrs_peacock"][1])
        screen.blit(board.mrs_white,self.suspect_dict["mrs_white"][1])
        screen.blit(board.prof_plum,self.suspect_dict["prof_plum"][1])

        screen.blit(board.candlestick,self.weapon_dict["candlestick"][1])
        screen.blit(board.dagger,self.weapon_dict["dagger"][1])
        screen.blit(board.lead_pipe,self.weapon_dict["lead_pipe"][1])
        screen.blit(board.revolver,self.weapon_dict["revolver"][1])
        screen.blit(board.rope,self.weapon_dict["rope"][1])
        screen.blit(board.wrench,self.weapon_dict["wrench"][1])

        # Initialize Rooms choices
        screen.blit(board.study_room_surface_accuse,self.room_dict["study_room"][1])
        screen.blit(board.lounge_surface_accuse,self.room_dict["lounge"][1])
        screen.blit(board.conservatory_surface_accuse,self.room_dict["conservatory"][1])
        screen.blit(board.kitchen_surface_accuse,self.room_dict["kitchen"][1])

        screen.blit(board.hall_surface_accuse,self.room_dict["hall"][1])
        screen.blit(board.library_surface_accuse,self.room_dict["library"][1])
        screen.blit(board.dining_room_surface_accuse,self.room_dict["dining_room"][1])
        screen.blit(board.ballroom_surface_accuse,self.room_dict["ballroom"][1])
        screen.blit(board.billiard_room_surface_accuse,self.room_dict["billiard_room"][1])

    def load_suggest_board(self, screen, board):

        # Initialize weapon and suspect choices
        screen.blit(board.colonel_mustard,self.suspect_dict["colonel_mustard"][1])
        screen.blit(board.miss_scarlet,self.suspect_dict["miss_scarlet"][1])
        screen.blit(board.mr_green,self.suspect_dict["mr_green"][1])
        screen.blit(board.mrs_peacock,self.suspect_dict["mrs_peacock"][1])
        screen.blit(board.mrs_white,self.suspect_dict["mrs_white"][1])
        screen.blit(board.prof_plum,self.suspect_dict["prof_plum"][1])

        screen.blit(board.candlestick,self.weapon_dict["candlestick"][1])
        screen.blit(board.dagger,self.weapon_dict["dagger"][1])
        screen.blit(board.lead_pipe,self.weapon_dict["lead_pipe"][1])
        screen.blit(board.revolver,self.weapon_dict["revolver"][1])
        screen.blit(board.rope,self.weapon_dict["rope"][1])
        screen.blit(board.wrench,self.weapon_dict["wrench"][1])

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

        room_options = Options_Box.Options_Box()
        if (state == "MOVING"):
            return room_options.draw_room_options(screen)
        if (state == "SUGGESTION"):
            return room_options.draw_suggest_options(screen)
        else :
            print("No options box drawed")
    
    def close_room_options(self, screen, color):

        room_options = Options_Box.Options_Box()
        room_options.close_option(screen, color)

    def get_tiles_directory(self) :
        return self.tile_rect_dict
    
    def get_weapon_directory(self) :
        return self.weapon_dict

    def get_suspect_directory(self) :
        return self.suspect_dict
    
    def get_room_directory(self) :
        return self.room_dict
    
    def highlight_tile_rect(self, screen, color, tile_name):
        if (tile_name == 'All'):
            for key in self.tile_rect_dict:
                pygame.draw.rect(screen,color,self.tile_rect_dict[key][0],2)
        else:
            pygame.draw.rect(screen,color,self.tile_rect_dict[tile_name][0],2)

    def highlight_rect(self, screen, color, card_type, key_name):
        if (card_type == 'weapon'):
            pygame.draw.rect(screen,color,self.weapon_dict[key_name][0],2)
        if (card_type == 'suspect'):
            pygame.draw.rect(screen,color,self.suspect_dict[key_name][0],2)
        if (card_type == 'room'):
            pygame.draw.rect(screen,color,self.room_dict[key_name][0],2)

    def display_update(self, screen, text):
        my_font = pygame.font.SysFont(None, 30)
        text_surface = my_font.render(text, False, (0, 0, 0))
        screen.blit(text_surface, (100,100))