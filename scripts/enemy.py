import pygame
from scripts.entities import Entity
import random


class Enemy(Entity):
    def __init__(self,game, pos = None, image_key='enemy'):
        super().__init__(game, 
                         pos if pos != None else 
                         (random.randint(10, game.display.get_width()-10), 
                          random.randint(10, game.display.get_height()-10)), 
                          image_key
                          )