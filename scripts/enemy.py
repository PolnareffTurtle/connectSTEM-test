import pygame
from scripts.entities import Entity
from scripts.economy import Coin
from random import randint

class Enemy(Entity):
    def __init__(self,game,pos, health = 6, attack = 1):
        super().__init__(game, pos, 'enemy')
        self.health = health #change if want
        self.alive = True
        self.attack = attack
        self.pos = list(pos)

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

    def create_wave(game, wave_number, count = 5):
        enemies = []
        for i in range(count):
            #randomize enemy spawns
            x = randint(20, game.display.get_width() - 40)
            y = randint(20, game.display.get_height() - 40)

            #difficulty-scaling
            base_health = 6 + int(wave_number * 1.4)
            base_attack = 1 + int(wave_number * .56)

            #slightly randomize health
            health = base_health + randint(-1,2)
            attack = base_attack + randint(0, 1)

            enemies.append(Enemy(game, (x, y), health = health, attack = attack))
        return enemies