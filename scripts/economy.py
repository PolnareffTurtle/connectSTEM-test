# economy.py
import pygame
from scripts.entities import Entity

class Wallet:
    def __init__(self):
        self.balance = 0

    def add(self, amount):
        self.balance += amount

    def spend(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False


class Coin(Entity):
    def __init__(self, game, pos, value=5):
        super().__init__(game, pos, 'coin')
        self.value = value
        self.collected = False

    def collect(self):
        if not self.collected:
            self.collected = True
            self.game.wallet.add(self.value)

    def render(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)