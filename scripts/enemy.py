import pygame
from scripts.entities import Entity
from scripts.enums import WeaponType
from scripts.weapon import Weapon, CircleWeapon, LungeWeapon
import random

class Enemy(Entity):

    image_key = 'enemy'
    range = 100

    def __init__(self,game, pos=None, target:Entity=None):
        if not pos:
            pos = (random.randint(10, game.tilemap.width*game.tilemap.tile_size-10), 
                   random.randint(10, game.tilemap.height*game.tilemap.tile_size-10))

        super().__init__(game, pos)
        self.set_friction(200)
        self.target = target if target != None else game.player
        
    def update(self, dt):
        super().update(dt)

        if self.health <= 0:
            if self in self.game.entities:
                self.game.entities.remove(self)
            return
        self.weapon.update(dt)

class CircleEnemy(Enemy):

    def __init__(self,game, pos=None, target:Entity=None):
        super().__init__(game, pos, target)
        self.weapon = CircleWeapon(attack_power=10, attack_speed=1, attack_radius=30)

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

    def __init__(self,game, pos=None, target:Entity=None):
        super().__init__(game, pos, target)
        self.weapon = LungeWeapon(attack_power=200, attack_speed=0.3)

    def update(self, dt):
        direction = self.target.pos - self.pos # pygame.Vector2
        if direction.magnitude() < self.range:
            if direction.magnitude() != 0:
                direction = direction.normalize()
            self.weapon.use(self, direction=direction)
        super().update(dt)
