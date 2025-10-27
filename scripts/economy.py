# economy.py
import pygame
from scripts.entities import Entity

class Wallet:
    #stores and manages the player's currency.
    def __init__(self):
        self.balance = 0

    def add(self, amount):
    #to increase weapon balance
        self.balance += amount

    def spend(self, amount):
    #tries to spend currency and returns true if successful
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False


class Coin(Entity):
    #coin collectible, increase wallet bal when picked
    def __init__(self, game, pos, value=5):
        super().__init__(game, pos, 'coin')
        self.value = value
        self.collected = False

    def collect(self):
        #mark as collected, add to waller
        if not self.collected:
            self.collected = True
            self.game.wallet.add(self.value)

    def render(self, screen):
        #drw onlt if uncolleted
        if not self.collected:
            screen.blit(self.image, self.rect)