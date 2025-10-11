import pygame
from scripts.weapon import Weapon

class Entity:
    def __init__(self,game,pos,image_key,atk=1,atk_spd=1):
        self.image = game.assets[image_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.game = game
        self.weapon = Weapon(atk,atk_spd)
        self.velocity = pygame.math.Vector2(0,0)
    
    def set_velocity(self,velocity:pygame.math.Vector2):
        self.velocity = velocity

    def set_friction(self,friction:float):
        if friction <= 0:
            self.velocity = pygame.math.Vector2(0,0)
            self.friction = 0.1
        else:
            self.friction = friction #friction is time it takes to go from full speed to full speed/2

    def update(self, delta_time):
        self.rect.centerx += self.velocity.x * delta_time
        self.rect.centery += self.velocity.y * delta_time
        self.velocity *= pow(2, -delta_time / self.friction) #friction formula (idk if the math works?)
        if abs(self.velocity.x) < 0.1: self.velocity.x = 0
        if abs(self.velocity.y) < 0.1: self.velocity.y = 0
        pass

    def render(self,screen):
        screen.blit(self.image,self.rect)

    def attack(self):
        self.weapon.use()

