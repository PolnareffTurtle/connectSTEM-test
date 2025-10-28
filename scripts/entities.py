import pygame
from scripts.weapon import Weapon

class Entity:
    #important
    def __init__(self,game,pos,image_key,atk=1,atk_spd=1):
        self.image = game.assets[image_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.game = game
        self.weapon = Weapon(atk,atk_spd)
    
    def render(self,screen):
        screen.blit(self.image,self.rect)

    def attack(self):
        self.weapon.use()

