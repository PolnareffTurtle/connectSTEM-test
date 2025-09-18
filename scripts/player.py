import pygame
from scripts.entities import Entity

class Player(Entity):
    def __init__(self,game,pos):
        super().__init__(game, pos, 'player')
        self.speed = 5
        self.max_health = 100
        self.health = 100

    def update(self,movement):
        self.rect.x += movement[0] * self.speed
        self.rect.y += movement[1] * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        # use the internal display surface for bounds checks (rendering is to `game.display`)
        if self.rect.right > self.game.display.get_width():
            self.rect.right = self.game.display.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.game.display.get_height():
            self.rect.bottom = self.game.display.get_height()
