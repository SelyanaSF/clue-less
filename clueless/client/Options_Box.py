import pygame
from pathlib import Path

class Options_Box:


    data_folder = Path("clueless/data/graphics/")

    def __init__ (self):

        # Initialize enter button, close button and text
        self.enter_image = pygame.image.load(self.data_folder / 'enter.PNG').convert_alpha()
        self.enter_image = pygame.transform.scale(self.enter_image, (55, 30))

        self.close_image = pygame.image.load(self.data_folder / 'close.PNG').convert_alpha()
        self.close_image = pygame.transform.scale(self.close_image, (15, 15))
        # mousePos = pygame.mouse.get_pos()
        # print(mousePos)
    
    def draw_room_options(self, screen):

        X_Pos = 800
        Y_Pos = 400
        WIDTH = 200
        HEIGHT = 200
        room_rect = pygame.Rect(X_Pos, Y_Pos, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (202, 228, 241), room_rect, width=0, border_radius=5)

        enter_rect = self.enter_image.get_rect()
        enter_rect.topleft = (X_Pos + 10, Y_Pos + 160)

        close_rect = self.enter_image.get_rect()
        close_rect.topleft = (X_Pos + 170, Y_Pos + 170)

        screen.blit(self.enter_image, (enter_rect.x, enter_rect.y))
        screen.blit(self.close_image, (close_rect.x, close_rect.y))

        message_font = pygame.font.SysFont('Comic Sans MS', 14)
        message_surface = message_font.render('Please click the tile you', False, (120,39,64))
        message_surface2 = message_font.render('choose and click Enter', False, (120,39,64))
        message_surface_rect = message_surface.get_rect(topleft = (X_Pos + 10, Y_Pos + 10))
        message_surface_rect2 = message_surface2.get_rect(topleft = (X_Pos + 10, Y_Pos + 25))

        screen.blit(message_surface, message_surface_rect)
        screen.blit(message_surface2, message_surface_rect2)

    def draw_suggest_options(self, screen):

        X_Pos = 780
        Y_Pos = 450
        WIDTH = 250
        HEIGHT = 70
        room_rect = pygame.Rect(X_Pos, Y_Pos, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (202, 228, 241), room_rect, width=0, border_radius=5)

        message_font = pygame.font.SysFont('Comic Sans MS', 14)
        message_surface = message_font.render('Please choose the suspect and', False, (120,39,64))
        message_surface2 = message_font.render('weapon. Then, click Submit', False, (120,39,64))
        message_surface_rect = message_surface.get_rect(topleft = (X_Pos + 10, Y_Pos + 10))
        message_surface_rect2 = message_surface2.get_rect(topleft = (X_Pos + 10, Y_Pos + 25))

        screen.blit(message_surface, message_surface_rect)
        screen.blit(message_surface2, message_surface_rect2)

    def close_option(self, screen, color):  
        X_Pos = 650
        Y_Pos = 400
        WIDTH = 200
        HEIGHT = 200
        room_rect = pygame.Rect(X_Pos, Y_Pos, WIDTH, HEIGHT)  
        pygame.draw.rect(screen, color, room_rect, width=0, border_radius=5)
        
        





        






