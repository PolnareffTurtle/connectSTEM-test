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
        # Assuming 'picker' has an attribute 'currency' to hold the amount of coins
        self.game.currency += self.value
        # Remove the coin from the game world
        self.game.CoinList.remove(self)
