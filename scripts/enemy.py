import math

import pygame
from scripts.entities import Entity
from scripts.enums import WeaponType
from scripts.weapon import Weapon, CircleWeapon, LungeWeapon, RotateWeapon
import random
from scripts.economy import Coin
from random import randint

class Enemy(Entity):
    image_key = 'enemy'
    range = 100
    value = 1

    def __init__(self,scene, pos=None, target:Entity=None, max_health: int = 100, attack: int = 5):
        if not pos:
            pos = (random.randint(10, scene.tilemap.width*scene.tilemap.tile_size-10), 
                   random.randint(10, scene.tilemap.height*scene.tilemap.tile_size-10))

        super().__init__(scene, pos)
        self.set_friction(200)
        self.target = target if target != None else scene.player

        self.max_health = max_health
        self.health = max_health
        self.attack = attack
        
    def update(self, dt):
        super().update(dt)

        if self.health <= 0:
            if self in self.scene.EnemyList:
                self.on_death()
                self.scene.EnemyList.remove(self)
            return
        self.weapon.update(dt)

    def on_death(self):
        # drop a coin on death
        drop_pos = (self.pos[0] + randint(-3, 3), self.pos[1] + randint(-3, 3))
        coin = Coin(self.scene, drop_pos)
        if not hasattr(self.scene, 'coins'):
            self.scene.coins = []
        self.scene.coins.append(coin)
    
    @staticmethod
    def create_wave(scene, wave_number, count = None):
        if not count:
            count = int(min(3 + .8 * wave_number + .04 * wave_number ** 2, 28))
        enemies = [] #to create and return list of enemies per wave
        for i in range(count):
            #scales attack & health w/ wave
            health = 5 + wave_number * 2
            attack = 1 + wave_number//2
            #random spawn positions
            pos = (randint(50, scene.game.display.get_width() - 50),
                   randint(50, scene.game.display.get_height() -50))

            enemies.append(RotateEnemy(scene, pos, max_health=health, attack=attack))
        return enemies


class CircleEnemy(Enemy):

    def __init__(self,scene, pos=None, max_health: int = 100, target:Entity=None, attack: int = 5):
        super().__init__(scene, pos, target, max_health=max_health, attack=attack)
        self.weapon = CircleWeapon(attack_power=10, attack_speed=1, attack_radius=30)
        self.value = 3

    def update(self, dt):
        self.weapon.use(self, targets=[self.target])
        super().update(dt)
    
    def render(self,screen,offset=(0,0)):
        
        # this is a pulsing circle to show the attack radius
        if self.weapon.last_attack and self.weapon.last_attack + 500 > pygame.time.get_ticks():
            # pygame is weird and requires surfaces for alpha
            surface = pygame.Surface((self.weapon.attack_radius*2,self.weapon.attack_radius*2),pygame.SRCALPHA)
            alpha = 200 - int(200 * (pygame.time.get_ticks() - self.weapon.last_attack) / 500)
            pygame.draw.circle(surface, (255,0,0,alpha), 
                               (self.weapon.attack_radius,self.weapon.attack_radius), 
                               self.weapon.attack_radius)
            screen.blit(surface, self.pos-offset-(self.weapon.attack_radius,self.weapon.attack_radius))
        super().render(screen,offset)
    

class LungeEnemy(Enemy):

    def __init__(self,scene, pos=None, target:Entity=None,  max_health: int = 100, attack: int = 5):
        super().__init__(scene, pos, target, max_health, attack)
        self.weapon = LungeWeapon(attack_power=200, attack_speed=0.3)
        self.value = 5

    def update(self, dt):
        direction = self.target.pos - self.pos # pygame.Vector2
        if direction.magnitude() < self.range:
            if direction.magnitude() != 0:
                direction = direction.normalize()
            self.weapon.use(self, direction=direction)
        super().update(dt)


class RotateEnemy(Enemy):

    def __init__(self, scene, pos = None, target: Entity = None,  max_health: int = 100, attack: int = 5):
        super().__init__(scene, pos, target, max_health=max_health, attack=attack)

        self.weapon = RotateWeapon(attack_power = 5, attack_speed = 1.5, radius = 45, rotation_speed = 240)
        self.value = 5

    def update(self, dt):
        super().update(dt)
        self.weapon.update(dt)
        self.weapon.attack(self, targets = [self.target])

    def render(self, screen, offset = (0, 0)):
        center = self.pos - offset

        # circle path
        pygame.draw.circle(screen, (0, 0, 0), (int(center.x), int(center.y)), int(self.weapon.radius), 1)

        # draw blade (line + circle)
        blade_pos = pygame.Vector2(center.x + math.cos(math.radians(self.weapon.angle)) * self.weapon.radius, center.y + math.sin(math.radians(self.weapon.angle)) * self.weapon.radius)

        pygame.draw.circle(screen, (255, 50, 50), (int(blade_pos.x), int(blade_pos.y)), 3)
        pygame.draw.line(screen, (255, 100, 100), blade_pos, center, 2)
        super().render(screen, offset)


