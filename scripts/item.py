import pygame
from scripts.enums import ItemType
from scripts.collide import Collide
class Item(Collide):
    
    type= ItemType.NONE

    def __init__(self, scene, startPos, autoPickup: bool = True):
        super().__init__(scene, self.image_key, startPos)
        self.autoPickup = autoPickup #if the item should be picked up automatically on contact
        