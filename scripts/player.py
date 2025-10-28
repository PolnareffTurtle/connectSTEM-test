import pygame
from math import sqrt
from scripts.entities import Entity
from scripts.enums import WeaponType

class Player(Entity):
    
    image_key = 'player'

    def __init__(self,game,pos):
        super().__init__(game, pos)
        self.speed = 100
        self.max_health = 100
        self.health = 100

    def update(self,movement: tuple[int,int],dt):
        self.set_velocity(pygame.math.Vector2(movement))
        if self.velocity.magnitude() != 0:
            self.velocity.scale_to_length(self.speed)
        
        for coin in self.game.CoinList:
            if self.aabb_collide(coin.rect()):
                coin.pickup()
        
        super().update(dt)
