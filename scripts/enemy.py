import pygame
from scripts.entities import Entity
import random

range = 50
class Enemy(Entity):
    def __init__(self,game, pos = None, image_key='enemy', target:Entity = None):
        super().__init__(game, 
                         pos if pos != None else 
                         (random.randint(10, game.display.get_width()-10), 
                          random.randint(10, game.display.get_height()-10)), 
                          image_key,
                          WeaponType= 'lunge'
                          )
        self.set_friction(5)
        self.target = target if target != None else game.player
        
    def update(self, delta_time):
        super().update(delta_time)
        self.weapon.update(delta_time)
        dist = ((self.target.rect.centerx - self.rect.centerx)**2 +
                (self.target.rect.centery - self.rect.centery )**2
                )**0.5
        if (dist < range and 
            (self.target.rect.centery != self.rect.centery or 
            self.target.rect.centerx != self.rect.centerx)):
            self.weapon.use(self, pygame.math.Vector2((self.target.rect.centerx - self.rect.centerx), (self.target.rect.centery - self.rect.centery)).normalize())
        pass