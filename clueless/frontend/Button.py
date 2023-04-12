import pygame

class Button:

    def __init__(self, x, y, w, h, color, highlightColor, font, text, selected = 0):
        self.color = color
        self.highlightColor = highlightColor
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = text
        self.selected = selected
        self.menuActive = False
        self.activeOption = -1
        self.clicked = False

    def draw(self, screen):
        action = False
        # draw rounded rectange, render the first text then add to screen
        pygame.draw.rect(screen, self.highlightColor 
                         if self.menuActive 
                         else self.color, self.rect, width=0, border_radius=5)
        msg = self.font.render(self.text, 1, (0, 0, 0))
        screen.blit(msg, msg.get_rect(center = self.rect.center))

        # get mouse position and check whether mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pos)
        if self.rect.collidepoint(mouse_pos):
            self.menuActive = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 1:
            self.clicked = False
        
        return action
