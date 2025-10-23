import math
import pygame
from scripts import enums
import random


# This isn't limited to traditional "weapons" 
# but instead is a classifier for how the entity attacks

class Weapon:

    type = None

    def __init__(self,attack_power: int = 1,attack_speed: float = 1):
        self.attack_power = attack_power 
        self.attack_speed = attack_speed 
        self.cooldown = 0
        self.last_attack = None
    
    def update(self, delta_time: float):
        if self.cooldown > 0:
            self.cooldown -= delta_time * random.uniform(0.8,1.2)
        if self.cooldown < 0:
            self.cooldown = 0

    def use(self, user, direction: pygame.Vector2 = None, targets: list = []):
        if self.cooldown <= 0:
            self.cooldown = 1 / self.attack_speed
            self.last_attack = pygame.time.get_ticks()
            self.attack(user, direction, targets)
    
    def attack(self, user, direction=None, targets: list = []):
        for target in targets:
            target.health -= self.attack_power
            target.health = max(0, target.health)

class CircleWeapon(Weapon):

    type = enums.WeaponType.CIRCLE

    def __init__(self, attack_power, attack_speed, attack_radius=25):
        super().__init__(attack_power, attack_speed)
        self.attack_radius = attack_radius
        self.last_circle_attack = 0

    def attack(self, user, direction=None, targets: list = []):
        in_range = []
        for target in targets:
            if self.attack_radius >= user.pos.distance_to(target.pos):
                in_range.append(target)
        super().attack(user, targets=in_range)
        

class LungeWeapon(Weapon):

    type = enums.WeaponType.LUNGE

    def __init__(self, attack_power, attack_speed):
        super().__init__(attack_power, attack_speed)

    def attack(self, user, direction, targets: list = []):
        user.velocity = direction * self.attack_power
