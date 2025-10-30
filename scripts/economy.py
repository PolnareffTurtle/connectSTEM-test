# economy.py
import pygame
from scripts.item import Item

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


class Coin(Item):

    image_key = 'coin'

    def __init__(self, scene, pos, value=5):
        super().__init__(scene, pos, autoPickup=True)
        self.value = value
        self.collected = False

    def collect(self):
        if not self.collected:
            self.collected = True
            self.scene.game.wallet.add(self.value)

    def render(self, screen, offset):
        if not self.collected:
            super().render(screen, offset)
