import pygame, random, os

# klasa tekst
class Text:
    def __init__(self, text, text_colour, size = 74):
        self.text = text
        self.text_colour = text_colour
        self.font = pygame.font.SysFont(None, size)
        self.image = self.font.render(str(self.text), 1, self.text_colour)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
