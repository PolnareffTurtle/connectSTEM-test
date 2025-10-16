import pygame
from scripts.entities import Entity
import random

range = 100
class Enemy(Entity):
    def __init__(self,game, pos=None, image_key='enemy', target:Entity=None):
        if not pos:
            pos = (random.randint(10, game.tilemap.width*game.tilemap.tile_size-10), 
                   random.randint(10, game.tilemap.height*game.tilemap.tile_size-10))

        super().__init__(game, pos, image_key, atk=50, WeaponType='lunge')
        self.set_friction(50)
        self.target = target if target != None else game.player
        
    def update(self, dt):
        super().update(dt)
        self.weapon.update(dt)
        dist = ((self.target.pos[0] - self.pos[0])**2 +
                (self.target.pos[1] - self.pos[1])**2
                )**0.5
        if (dist < range and self.target.pos != self.pos):
            direction = pygame.math.Vector2((self.target.pos[0] - self.pos[0]), (self.target.pos[1] - self.pos[1])).normalize()
            self.weapon.use(user=self, direction=direction)
