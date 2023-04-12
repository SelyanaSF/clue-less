import pygame
from pathlib import Path

class Weapon_Image:

    def __init__(self):
        pass

    def display_weapon_image(self, weapon_image):

        pygame.init()
        data_folder = Path("clueless/data/graphics/")

        # Load the image and scale it down to fit the window
        image = pygame.image.load(data_folder/weapon_image)
        scaled_image = pygame.transform.scale(image, (600,500))

        # Create the Pygame window
        screen = pygame.display.set_mode((600,500))
        pygame.display.set_caption('Weapon Image')

        # Center the image on the screen
        imagerect = scaled_image.get_rect()
        imagerect.center = screen.get_rect().center
        

        while True:
            screen.fill('white')
            screen.blit(scaled_image, imagerect) # using the rect object
            #screen. blit (image,(0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()


# Note that this Class is called in Game.py

