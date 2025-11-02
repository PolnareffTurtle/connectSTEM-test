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


