import pygame
from scripts.weapon import Weapon

class Entity:
    def __init__(self,game,pos,image_key,atk=1,atk_spd=1):
        self.image = game.assets[image_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = list(pos)
        self.game = game
        self.weapon = Weapon(atk,atk_spd)
    
    def render(self,screen,offset=(0,0)):
        rect = self.rect()
        screen.blit(self.image,(rect.x-offset[0],rect.y-offset[1]))

    def attack(self):
        self.weapon.use()

    def rect(self):
        return self.image.get_rect(center=self.pos)

