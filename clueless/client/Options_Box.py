import pygame
from pathlib import Path

class Options_Box:

    X_Pos = 650
    Y_Pos = 400
    WIDTH = 200
    HEIGHT = 200
    data_folder = Path("clueless/data/graphics/")

    def __init__ (self):

        
        self.rect = pygame.Rect(self.X_Pos, self.Y_Pos, self.WIDTH, self.HEIGHT)
        # Initialize enter button, close button and text
        self.enter_image = pygame.image.load(self.data_folder / 'enter.PNG').convert_alpha()
        self.enter_image = pygame.transform.scale(self.enter_image, (55, 30))
        self.enter_rect = self.enter_image.get_rect()
        self.enter_rect.topleft = (self.X_Pos + 10, self.Y_Pos + 160)

        self.close_image = pygame.image.load(self.data_folder / 'close.PNG').convert_alpha()
        self.close_image = pygame.transform.scale(self.close_image, (15, 15))
        self.close_rect = self.enter_image.get_rect()
        self.close_rect.topleft = (self.X_Pos + 170, self.Y_Pos + 170)
        mousePos = pygame.mouse.get_pos()
        print(mousePos)
    
    def draw_room_options(self, screen):
        
        pygame.draw.rect(screen, (202, 228, 241), self.rect, width=0, border_radius=5)

        screen.blit(self.enter_image, (self.enter_rect.x, self.enter_rect.y))
        screen.blit(self.close_image, (self.close_rect.x, self.close_rect.y))

        message_font = pygame.font.SysFont('Comic Sans MS', 14)
        message_surface = message_font.render('Please click the room you', False, (120,39,64))
        message_surface2 = message_font.render('choose and click Enter', False, (120,39,64))
        message_surface_rect = message_surface.get_rect(topleft = (self.X_Pos + 10, self.Y_Pos + 10))
        message_surface_rect2 = message_surface2.get_rect(topleft = (self.X_Pos + 10, self.Y_Pos + 25))

        screen.blit(message_surface, message_surface_rect)
        screen.blit(message_surface2, message_surface_rect2)

        return [self.enter_rect, self.close_rect]
    
    def draw_accuse_options(self, screen, events):
        
        pygame.draw.rect(screen, (202, 228, 241), self.rect, width=0, border_radius=5)

        screen.blit(self.enter_image, (self.enter_rect.x, self.enter_rect.y))
        screen.blit(self.close_image, (self.close_rect.x, self.close_rect.y))

        # COLOR_INACTIVE = (100, 80, 255)
        # COLOR_ACTIVE = (100, 200, 255)
        # COLOR_LIST_INACTIVE = (255, 100, 100)
        # COLOR_LIST_ACTIVE = (255, 150, 150)

        # weapon_list = Dropdown.Dropdown(
        #     [COLOR_INACTIVE, COLOR_ACTIVE],
        #     [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        #     660, 450, 110, 20, 
        #     pygame.font.SysFont(None, 20), 
        #     "Select Weapon", ["Dagger", "Gun"])
        
        # selected_option = weapon_list.update(events)
        # if selected_option >= 0:
        #     weapon_list.main = weapon_list.options[selected_option]

        # weapon_list.draw(screen)

        message_font = pygame.font.SysFont('Comic Sans MS', 14)
        message_surface = message_font.render('Please choose final weapon,', False, (120,39,64))
        message_surface2 = message_font.render('room, and murderer', False, (120,39,64))
        message_surface_rect = message_surface.get_rect(topleft = (self.X_Pos + 10, self.Y_Pos + 10))
        message_surface_rect2 = message_surface2.get_rect(topleft = (self.X_Pos + 10, self.Y_Pos + 25))

        screen.blit(message_surface, message_surface_rect)
        screen.blit(message_surface2, message_surface_rect2)

        return [self.enter_rect, self.close_rect]
    
    def draw_suggest_options(self, screen):
        
        pygame.draw.rect(screen, (202, 228, 241), self.rect, width=0, border_radius=5)

        screen.blit(self.enter_image, (self.enter_rect.x, self.enter_rect.y))
        screen.blit(self.close_image, (self.close_rect.x, self.close_rect.y))

        message_font = pygame.font.SysFont('Comic Sans MS', 14)
        message_surface = message_font.render('Please suggest weapon,', False, (120,39,64))
        message_surface2 = message_font.render('room, and murderer', False, (120,39,64))
        message_surface_rect = message_surface.get_rect(topleft = (self.X_Pos + 10, self.Y_Pos + 10))
        message_surface_rect2 = message_surface2.get_rect(topleft = (self.X_Pos + 10, self.Y_Pos + 25))

        screen.blit(message_surface, message_surface_rect)
        screen.blit(message_surface2, message_surface_rect2)

        return [self.enter_rect, self.close_rect]

    def close_option(self, screen, color):    
        pygame.draw.rect(screen, color, self.rect, width=0, border_radius=5)
        
        





        






