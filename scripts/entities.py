import pygame
from scripts.weapon import Weapon
from scripts.collide import Collide
sign = lambda x: (x>0) - (x<0)

class Entity(Collide):

    image_key = None

    def __init__(self,game,pos: tuple[float,float]):
        super().__init__(game, self.image_key, pos)
        self.velocity = pygame.math.Vector2(0,0)
        self.friction = 0
 
    def set_velocity(self,velocity:pygame.math.Vector2):
        self.velocity = velocity

    def set_friction(self,friction:float):
        self.friction = friction 

    def check_collisions(self,rects, prev_movement: tuple = (0,0)):
        # AABB collision detection without using rects (preserves float position since rects use integers)
        for rect in rects:
            if self.aabb_collide(rect): 
                if prev_movement[0] > 0:
                    self.pos.x = rect.left - self.size[0]/2
                elif prev_movement[0] < 0:
                    self.pos.x = rect.right + self.size[0]/2
                if prev_movement[1] > 0:
                    self.pos.y = rect.top - self.size[1]/2
                elif prev_movement[1] < 0:
                    self.pos.y = rect.bottom + self.size[1]/2

    def update(self, dt):
        tilemap = self.game.tilemap
        physics_rects = tilemap.physics_rects_around(self.pos)

        # apply velocity and check for collisions (x and y separately)
        self.pos.x += self.velocity.x * dt
        self.check_collisions(physics_rects, (self.velocity.x * dt,0))
        self.pos.y += self.velocity.y * dt
        self.check_collisions(physics_rects, (0,self.velocity.y * dt))

        # check for bounds using self.pos and self.size
        if self.pos.x - self.size[0]/2 < 0:
            self.pos.x = self.size[0]/2
            self.velocity.x = 0
        if self.pos.x + self.size[0] > tilemap.width * tilemap.tile_size:
            self.pos.x = tilemap.width * tilemap.tile_size + self.size[0]/2
            self.velocity.x = 0
        if self.pos.y - self.size[1]/2 < 0:
            self.pos.y = self.size[1]/2
            self.velocity.y = 0
        if self.pos.y + self.size[1]/2 > tilemap.height * tilemap.tile_size:
            self.pos.y = tilemap.height * tilemap.tile_size + self.size[1]/2
            self.velocity.y = 0

        # apply friction
        if self.friction != 0:
            self.velocity.x -= sign(self.velocity.x)*self.friction * dt
            self.velocity.y -= sign(self.velocity.y)*self.friction * dt

        # clamp very small velocities to 0
        if self.velocity.magnitude() < 1:
            self.velocity = pygame.math.Vector2(0,0)
        if self.velocity.magnitude() == 0:
            self.pos = pygame.math.Vector2(round(self.pos.x),round(self.pos.y))

    #should be extended by subclasses
    def on_death(self):
        pass