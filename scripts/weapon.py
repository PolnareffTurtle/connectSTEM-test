import pygame
from enum import Enum
from scripts import enums
def circle_attack(atk_power):
    pass

# This isn't limited to traditional "weapons" 
# but instead is a classifier for how the entity attacks
class Weapon:
    def __init__(self,attack_power,attack_speed,attack_size = 1,type = enums.WeaponType.NONE):
        self.attack_power = attack_power
        self.attack_speed = attack_speed
        self.attack_size = attack_size 
        self.type = type
        self.cooldown = 0

    def update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time
        if self.cooldown < 0:
            self.cooldown = 0
        pass

    def use(self, user, direction):
        if self.cooldown > 0:
            return
        match self.type:
            case 'circle':
                circle_attack(self.attack_power, self.attack_size)
            case 'projectile':
                pass
            case 'lunge':
                self.lunge_attack(user, direction)
                pass
            case _:
                print("Unknown weapon type")
        pass

    def lunge_attack(self, user, direction):
        user.velocity = direction * self.attack_power
        print("lunger")
        cooldown = 10
        pass

