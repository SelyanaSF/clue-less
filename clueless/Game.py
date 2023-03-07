# Game Module
from sys import exit
from clueless import Board
import pygame


class Game:
    WIDTH = 700
    HEIGHT = 700
    FPS = 60

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Clue-Less")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.events()

    def events(self) :
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.add_board()
            self.render()
            self.tick()

    def add_board(self):
        # Add board
        board = Board.Board()
        self.screen.blit(board.boardSurface,(75,75))

        self.screen.blit(board.hallwayVertical,(125,200))
        self.screen.blit(board.hallwayVertical,(325,200))
        self.screen.blit(board.hallwayVertical,(525,200))
        self.screen.blit(board.hallwayVertical,(125,400))
        self.screen.blit(board.hallwayVertical,(325,400))
        self.screen.blit(board.hallwayVertical,(525,400))

        self.screen.blit(board.hallway,(200,125))
        self.screen.blit(board.hallway,(400,125))
        self.screen.blit(board.hallway,(200,325))
        self.screen.blit(board.hallway,(400,325))
        self.screen.blit(board.hallway,(200,525))
        self.screen.blit(board.hallway,(400,525))

        self.screen.blit(board.cornerRoomSurface,(100,100))
        self.screen.blit(board.cornerRoomSurface,(500,100))
        self.screen.blit(board.cornerRoomSurface,(100,500))
        self.screen.blit(board.cornerRoomSurface,(500,500))

        self.screen.blit(board.normalRoomSurface,(300,100))
        self.screen.blit(board.normalRoomSurface,(100,300))
        self.screen.blit(board.normalRoomSurface,(500,300))
        self.screen.blit(board.normalRoomSurface,(300,500))
        self.screen.blit(board.normalRoomSurface,(300,300))


    def render(self):
        pygame.display.update()

    def tick(self):
        self.clock.tick(self.FPS)