import pygame
from scripts.entities import Entity
from scripts.economy import Coin
from random import randint

class Enemy(Entity):
    def __init__(self,game,pos):
        super().__init__(game, pos, 'enemy')
        self.health = 1  #change if want
        self.alive = True

    def die(self):
        #drop coin when enemy die
        if not self.alive:
            return
        self.alive = False
        drop_pos = (self.pos[0] + randint(-3, 3), self.pos[1] + randint(-3, 3))
        coin = Coin(self.game, drop_pos)
        if not hasattr(self.game, 'coins'):
            self.game.coins = []
        self.game.coins.append(coin)