import pygame

class Enemy:
    def __init__(self,game,pos):
        self.image = game.assets['enemy']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.game = game
    
    def render(self,screen):
        screen.blit(self.image,self.rect)


"""
Implement the enemy class here!
"""
