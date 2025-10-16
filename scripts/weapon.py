import math
import pygame

def circle_attack(self, owner, target, game):
    now = pygame.time.get_ticks()
    cooldown = 1500 / self.attack_speed
    # print("last attack:", self.last_attack)
    # print("cooldown:", cooldown)
    # print("now:", now)
    delta_x = target.rect.centerx - owner.rect.centerx
    if self.last_attack + cooldown <= now:
        # print("last attack:", self.last_attack)

        target.health -= self.attack_power
        target.health = max(0, target.health)

        self.last_attack = now
        return True
    else:
        return False

class Weapon:
    def __init__(self,attack_power,attack_speed,attack_radius = 25,atk_method=None):
        self.attack_power = attack_power
        self.attack_speed = attack_speed
        self.attack_radius = attack_radius
        self.last_attack = -10000

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
