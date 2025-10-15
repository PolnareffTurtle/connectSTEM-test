import pygame
from scripts.weapon import Weapon

class Entity:
    def __init__(self,game,pos,image_key,atk=1,atk_spd=1,atk_size=1, WeaponType=None):
        self.image = game.assets[image_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.game = game
        self.weapon = Weapon(atk,atk_spd, atk_size, WeaponType)
        self.velocity = pygame.math.Vector2(0,0)
        self.friction = 0
    
    def set_velocity(self,velocity:pygame.math.Vector2):
        self.velocity = velocity

    def set_friction(self,friction:float):
        self.friction = friction 

    def update(self, delta_time):
        self.rect.centerx += self.velocity.x * delta_time
        self.rect.centery += self.velocity.y * delta_time

        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        if self.rect.right > self.game.display.get_width():
            self.rect.right = self.game.display.get_width()
            self.velocity.x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = 0
        if self.rect.bottom > self.game.display.get_height():
            self.rect.bottom = self.game.display.get_height()
            self.velocity.y = 0

        if self.friction != 0:
            if abs(self.velocity.x) < self.friction * delta_time:
                self.velocity.x = 0
            if abs(self.velocity.y) < self.friction * delta_time:
                self.velocity.y = 0
            if self.velocity.x > 0:
                self.velocity.x -= self.friction * delta_time
            elif self.velocity.x < 0:
                self.velocity.x += self.friction * delta_time
            if self.velocity.y > 0:
                self.velocity.y -= self.friction * delta_time
            elif self.velocity.y < 0:
                self.velocity.y += self.friction * delta_time

    def render(self,screen):
        screen.blit(self.image,self.rect)

    def attack(self):
        self.weapon.use()

