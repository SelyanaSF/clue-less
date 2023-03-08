# Board Module
import pygame
from pathlib import Path

class Board:
    WIDTH = 550
    HEIGHT = 550
    
    def __init__(self):
        self.boardSurface = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.boardSurface.fill('bisque3')
        data_folder = Path("clueless/data/graphics/")

        self.cornerRoomSurface = pygame.image.load(data_folder / 'corner.PNG')
        self.cornerRoomSurface = pygame.transform.scale(self.cornerRoomSurface, (100, 100))

        self.normalRoomSurface = pygame.image.load(data_folder / 'window.PNG')
        self.normalRoomSurface = pygame.transform.scale(self.normalRoomSurface, (100, 100))

        self.hallway = pygame.image.load(data_folder / 'hallway.PNG')
        self.hallway = pygame.transform.scale(self.hallway, (100, 50))

        self.hallwayVertical = pygame.transform.scale(self.hallway, (50, 100))

