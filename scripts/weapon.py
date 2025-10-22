import math
import pygame
from enum import Enum
from scripts import enums
import random


# This isn't limited to traditional "weapons" 
# but instead is a classifier for how the entity attacks

class Weapon:
    def __init__(self,attack_power,attack_speed,attack_size = 1,type = enums.WeaponType.NONE, attack_radius=25):
        self.attack_power = attack_power
        self.attack_speed = attack_speed
        self.attack_size = attack_size 
        self.type = type
        self.cooldown = 0
        self.attack_radius = attack_radius
        self.last_circle_attack = -10000
    
    def update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time * random.uniform(0.8,1.2)
        if self.cooldown < 0:
            self.cooldown = 0

    def use(self, user, direction=None, target=None):
        if self.cooldown > 0:
            return
        match self.type:
            case 'circle':
                self.circle_attack(user, target)
            case 'projectile':
                pass
            case 'lunge':
                self.lunge_attack(user, direction)
            case _:
                print("Unknown weapon type")
    
    def lunge_attack(self, user, direction):
        user.velocity = direction * self.attack_power
        self.cooldown = 5/self.attack_speed

    def circle_attack(self, user, target):
        self.last_circle_attack = pygame.time.get_ticks()
        self.cooldown = 3 / self.attack_speed
        if self.attack_radius >= math.sqrt((user.pos[0] - target.pos[0]) ** 2 + (user.pos[1] - target.pos[1]) ** 2):
            target.health -= self.attack_power
            target.health = max(0, target.health)

"""
def use(self, owner, target, game):
        delta_x = target.rect.centerx - owner.rect.centerx
        delta_y = target.rect.centery - owner.rect.centery
        distance = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

        if distance < self.attack_radius:
            print("used\n")
            return circle_attack(self, owner, target, game)
        return None
        # print("distance:", distance, end = " ")
        # print("health:", target.health)

"""
