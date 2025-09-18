import pygame
from scripts.entities import Entity

class Enemy(Entity):
    def __init__(self,game,pos):
        super().__init__(game, pos, 'enemy')