import pygame
from scripts.weapon import Weapon

sign = lambda x: (x>0) - (x<0)

class Entity:
    def __init__(self,game,pos,image_key,atk=1,atk_spd=1,atk_size=1, WeaponType=None):
        self.image = game.assets[image_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = list(pos)
        self.game = game
        self.weapon = Weapon(atk,atk_spd, atk_size, WeaponType)
        self.velocity = pygame.math.Vector2(0,0)
        self.friction = 0
    
    def render(self,screen,offset=(0,0)):
        rect = self.rect()
        screen.blit(self.image,(rect.x-offset[0],rect.y-offset[1]))

    def set_velocity(self,velocity:pygame.math.Vector2):
        self.velocity = velocity

    def set_friction(self,friction:float):
        self.friction = friction 

    def check_collisions(self,entity_rect,rects,prev_movement):
        for rect in rects:
            if rect.colliderect(entity_rect):
                if prev_movement[0] < 0:
                    entity_rect.left = rect.right
                    #self.velocity.x = 0
                elif prev_movement[0] > 0:
                    entity_rect.right = rect.left
                    #self.velocity.x = 0
                if prev_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    #self.velocity.y = 0
                elif prev_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    #self.velocity.y = 0

    def update(self, dt):
        tilemap = self.game.tilemap
        entity_rect = self.rect()
        physics_rects = tilemap.physics_rects_around(self.pos)

        # apply velocity and check for collisions (x and y separately)
        entity_rect.x += self.velocity.x * dt
        self.check_collisions(entity_rect,physics_rects,[self.velocity.x,0])
        entity_rect.y += self.velocity.y * dt
        self.check_collisions(entity_rect,physics_rects,[0,self.velocity.y])

        # check for bounds
        if entity_rect.left < 0:
            entity_rect.left = 0
            self.velocity.x = 0
        if entity_rect.right > tilemap.width * tilemap.tile_size:
            entity_rect.right = tilemap.width * tilemap.tile_size
            self.velocity.x = 0
        if entity_rect.top < 0:
            entity_rect.top = 0
            self.velocity.y = 0
        if entity_rect.bottom > tilemap.height * tilemap.tile_size:
            entity_rect.bottom = tilemap.height * tilemap.tile_size
            self.velocity.y = 0

        # update position
        self.pos = [entity_rect.centerx,entity_rect.centery]

        # apply friction
        if self.friction != 0:
            if abs(self.velocity.x) < self.friction * dt:
                self.velocity.x = 0
            if abs(self.velocity.y) < self.friction * dt:
                self.velocity.y = 0
            self.velocity.x -= sign(self.velocity.x)*self.friction * dt
            self.velocity.y -= sign(self.velocity.y)*self.friction * dt

    def attack(self):
        self.weapon.use()

    def rect(self):
        return self.image.get_rect(center=self.pos)

