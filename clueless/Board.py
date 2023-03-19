# Board Module
import pygame
from clueless import Button, OptionsBox
from pathlib import Path

class Board:
    WIDTH = 550
    HEIGHT = 550
    boardYPos = 75
    boardXPos = 75
    # buttonYPos = 75
    # buttonXPos = 650
    
    def __init__(self):
        self.boardSurface = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.boardSurface.fill('bisque3')
        data_folder = Path("clueless/data/graphics/")

        self.cornerRoomSurface = pygame.image.load(data_folder / 'corner.PNG')
        self.cornerRoomSurface = pygame.transform.scale(self.cornerRoomSurface, (100, 100))
        self.cornerRoomRect = self.cornerRoomSurface.get_rect()

        self.normalRoomSurface = pygame.image.load(data_folder / 'window.PNG')
        self.normalRoomSurface = pygame.transform.scale(self.normalRoomSurface, (100, 100))
        self.normalRect = self.normalRoomSurface.get_rect()

        self.hallway = pygame.image.load(data_folder / 'hallway.PNG')
        self.hallway = pygame.transform.scale(self.hallway, (100, 50))
        self.hallwayRect = self.hallway.get_rect()

        self.hallwayVertical = pygame.transform.scale(self.hallway, (50, 100))
        self.hallwayVerticalRect = self.hallwayVertical.get_rect()
    
    def loadTiles(self, screen, board):

        screen.blit(board.boardSurface,(self.boardXPos,self.boardYPos))

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

        screen.blit(board.cornerRoomSurface,(100,100))
        screen.blit(board.cornerRoomSurface,(500,100))
        screen.blit(board.cornerRoomSurface,(100,500))
        screen.blit(board.cornerRoomSurface,(500,500))

        screen.blit(board.normalRoomSurface,(300,100))
        screen.blit(board.normalRoomSurface,(100,300))
        screen.blit(board.normalRoomSurface,(500,300))
        screen.blit(board.normalRoomSurface,(300,500))
        screen.blit(board.normalRoomSurface,(300,300))

    def loadButton(self, screen, text, buttonXPos, buttonYPos):
        buttonColor = (150, 150, 150)
        buttonWidth = 160
        buttonHeight = 40
        buttonHighlightColor = (100, 200, 255)
        buttonFont = pygame.font.SysFont(None, 30)

        goToRoomButton = Button.Button(buttonXPos, buttonYPos, buttonWidth, buttonHeight, buttonColor, buttonHighlightColor, buttonFont, text)
        goToRoomButton.draw(screen)
        return goToRoomButton.draw(screen)

    def loadRoomOptions(self, screen):

        roomOptions = OptionsBox.OptionsBox()
        return roomOptions.draw(screen)
    
    def closeRoomOptions(self, screen):

        roomOptions = OptionsBox.OptionsBox()
        roomOptions.closeOption(screen)

