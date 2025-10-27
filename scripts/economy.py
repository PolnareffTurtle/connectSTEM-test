# economy.py
import pygame
from scripts.entities import Entity

class Wallet:
    """Stores and manages the player's currency."""
    def __init__(self):
        self.balance = 0

    def add(self, amount):
        """Increase wallet balance."""
        self.balance += amount

    def spend(self, amount):
        """Try to spend currency; returns True if successful."""
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False


class Coin(Entity):
    """Collectible coin that increases wallet balance when picked up."""
    def __init__(self, game, pos, value=5):
        super().__init__(game, pos, 'coin')
        self.value = value
        self.collected = False

    def collect(self):
        """Mark as collected and add to player wallet."""
        if not self.collected:
            self.collected = True
            self.game.wallet.add(self.value)

    def render(self, screen):
        """Draw only if not collected."""
        if not self.collected:
            screen.blit(self.image, self.rect)
