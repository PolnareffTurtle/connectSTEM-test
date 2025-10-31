import pygame
from scripts.enums import ItemType
from scripts.collide import Collide
class Item(Collide):
    
    image_key = None
    type = ItemType.NONE

    def __init__(self, scene, startPos, autoPickup: bool = True):
        super().__init__(scene, self.image_key, startPos)
        self.autoPickup = autoPickup #if the item should be picked up automatically on contact

class Coin(Item):

    image_key = 'coin'
    type = ItemType.COIN

    def __init__(self, scene, pos, value=5):
        super().__init__(scene, pos, autoPickup=True)
        self.value = value
        self.collected = False

    def collect(self):
        if not self.collected:
            self.collected = True
            self.scene.wallet.add(self.value)

    def render(self, screen, offset):
        if not self.collected:
            super().render(screen, offset)
