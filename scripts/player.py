import pygame
from math import sqrt
from scripts.entities import Entity

class Player(Entity):
    def __init__(self,game,pos):
        super().__init__(game, pos, 'player')
        self.speed = 50
        self.max_health = 100
        self.health = 100

    def update(self,movement: tuple[int,int],dt):

        # normalize for speed moving diagonally 
        self.set_velocity(pygame.math.Vector2(movement))
        if self.velocity.magnitude() != 0:
            self.velocity.scale_to_length(self.speed)
        
        super().update(dt)
