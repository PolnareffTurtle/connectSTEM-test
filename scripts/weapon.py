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



class RotateWeapon(Weapon):
    type = enums.WeaponType.ROTATE

    def __init__(self, attack_power, attack_speed, radius = 40, rotation_speed = 180):
        super().__init__(attack_power, attack_speed)
        self.radius = radius
        self.rotation_speed = rotation_speed
        self.angle = 0
        self.last_attack = 0

    def update(self, delta_time: float):
        super().update(delta_time)
        # rotate
        self.angle = (self.angle + self.rotation_speed * delta_time) % 360

    def attack(self, user, targets: list = []):
        # translate to coords
        weapon_pos = pygame.Vector2(user.pos.x + math.cos(math.radians(self.angle)) * self.radius, user.pos.y + math.sin(math.radians(self.angle)) * self.radius)

        for target in targets:
            if target.pos.distance_to(weapon_pos) <= 15: # need better collision detection
                now = pygame.time.get_ticks()

                if now - self.last_attack > 250: # hard coded as well
                    target.health -= self.attack_power
                    target.health = max(0, target.health)
                    self.last_attack = now