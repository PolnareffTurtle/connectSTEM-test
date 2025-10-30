import pygame
from scripts.entities import Entity
from scripts.economy import Coin
from random import randint

class Enemy(Entity):
    image_key = 'enemy' #added to define spirte key
    def __init__(self, game, pos, health = 6, attack = 1):
        super().__init__(game, pos)
        self.health = health #scales w/ wave # later
        self.attack = attack #can scale for harder enemies
        self.alive = True

    def die(self):
        #drop coin when enemy die
        if not self.alive:
            return
        self.alive = False
        drop_pos = (self.pos[0] + randint(-3, 3), self.pos[1] + randint(-3, 3))
        coin = Coin(self.game, drop_pos)
        #ensure game can append to coin list
        if not hasattr(self.game, 'coins'):
            self.game.coins = []

        self.game.coins.append(coin)

    def create_wave(game, wave_number, count):
        enemies = [] #to create and return list of enemies per wave
        for i in range(count):
            #scales attack & health w/ wave
            health = 5 + wave_number * 2
            attack = 1 + wave_number//2
            #random spawn positions
            pos = (randint(50, game.display.get_width() - 50),
                   randint(50, game.display.get_height() -50))

            enemies.append(Enemy(game, pos, health, attack))
        return enemies