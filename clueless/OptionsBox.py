import pygame
from pathlib import Path

class OptionsBox:

    XPos = 650
    YPos = 400
    WIDTH = 200
    HEIGHT = 200
    data_folder = Path("clueless/data/graphics/")

    def __init__ (self):

        
        self.rect = pygame.Rect(self.XPos, self.YPos, self.WIDTH, self.HEIGHT)
        # Initialize enter button, close button and text
        self.enterImage = pygame.image.load(self.data_folder / 'enter.PNG').convert_alpha()
        self.enterImage = pygame.transform.scale(self.enterImage, (55, 30))
        self.enterRect = self.enterImage.get_rect()
        self.enterRect.topleft = (self.XPos + 10, self.YPos + 160)

        self.closeImage = pygame.image.load(self.data_folder / 'close.PNG').convert_alpha()
        self.closeImage = pygame.transform.scale(self.closeImage, (15, 15))
        self.closeRect = self.enterImage.get_rect()
        self.closeRect.topleft = (self.XPos + 170, self.YPos + 170)
        mousePos = pygame.mouse.get_pos()
        print(mousePos)
    
    def draw(self, screen):
        
        pygame.draw.rect(screen, (202, 228, 241), self.rect, width=0, border_radius=5)

        screen.blit(self.enterImage, (self.enterRect.x, self.enterRect.y))
        screen.blit(self.closeImage, (self.closeRect.x, self.closeRect.y))

        messageFont = pygame.font.SysFont('Comic Sans MS', 14)
        messageSurface = messageFont.render('Please click the room you', False, (120,39,64))
        messageSurface2 = messageFont.render('choose and click Enter', False, (120,39,64))
        messageSurfaceRect = messageSurface.get_rect(topleft = (self.XPos + 10, self.YPos + 10))
        messageSurfaceRect2 = messageSurface.get_rect(topleft = (self.XPos + 10, self.YPos + 25))

        screen.blit(messageSurface, messageSurfaceRect)
        screen.blit(messageSurface2, messageSurfaceRect2)

        return [self.enterRect, self.closeRect]

    def closeOption(self, screen, color):    
        pygame.draw.rect(screen, color, self.rect, width=0, border_radius=5)
        
        





        






