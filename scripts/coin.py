from scripts.item import Item;
from scripts.enums import ItemType
import pygame

class Coin(Item):
    
    type = ItemType.COIN
    image_key = 'CoinSprite(TEMP)'

    def __init__(self, game, startPos, value: int = 1):
        super().__init__(game, startPos, autoPickup=True)
        self.value = value

    def pickup(self):
        self.game.currency += self.value
        self.game.CoinList.remove(self)
