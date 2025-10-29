import pygame
from scripts.weapon import Weapon
from scripts.collide import Collide
from scripts.utils import Text

class HealthBar:
    def __init__(self, entity):
        self.entity = entity
    def draw(self, screen, offset):
        health_ratio = max(0, min(1, self.entity.health / self.entity.max_health))
        width = self.entity.size[0]
        x = int(self.entity.pos.x - width/2 - offset[0])
        y = int(self.entity.pos.y - self.entity.size[1]/2 - 10 - offset[1])

        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, 5))

        r = int(255 * (1 - health_ratio))
        g = int(255 * health_ratio)
        b = 0
        color = (r, g, b)
        pygame.draw.rect(screen, color, (x+1, y+1, int((width-2) * health_ratio), 3))


sign = lambda x: (x>0) - (x<0)

class Entity(Collide):

    image_key = None
    max_health = 100

    def __init__(self,game,pos: tuple[float,float]):
        super().__init__(game, self.image_key, pos)
        self.velocity = pygame.math.Vector2(0,0)
        self.friction = 0
        self.max_health = 100
        self.health = self.max_health
        self.healthbar = HealthBar(self)

    def render(self,screen,offset=(0,0)):
        rect = self.rect()
        screen.blit(self.image,(rect.x-offset[0],rect.y-offset[1]))
        self.healthbar.draw(screen, offset)

    def set_velocity(self,velocity:pygame.math.Vector2):
        self.velocity = velocity

    def set_friction(self,friction:float):
        self.friction = friction 

# AABB collision detection for tilemap
# note: do we want to 
    def check_wall_collisions(self,rects, prev_movement: tuple = (0,0)):
        for rect in rects:
            if self.aabb_collide(rect): 
                if prev_movement[0] > 0:
                    self.pos.x = rect.left - self.size[0]/2
                    self.velocity.x = 0
                elif prev_movement[0] < 0:
                    self.pos.x = rect.right + self.size[0]/2
                    self.velocity.x = 0
                if prev_movement[1] > 0:
                    self.pos.y = rect.top - self.size[1]/2
                    self.velocity.y = 0
                elif prev_movement[1] < 0:
                    self.pos.y = rect.bottom + self.size[1]/2
                    self.velocity.y = 0

#override of the update method to include collision and movement
    def update(self, dt):
        tilemap = self.game.tilemap
        physics_rects = tilemap.physics_rects_around(self.pos)

        # apply velocity and check for collisions (x and y separately)
        self.pos.x += self.velocity.x * dt
        self.check_wall_collisions(physics_rects, (self.velocity.x * dt,0))
        self.pos.y += self.velocity.y * dt
        self.check_wall_collisions(physics_rects, (0,self.velocity.y * dt))

        # turn of velocity if collision with world bounds or something idk. I don't rly know if we need this given we have check_wall_collisions
        if self.pos.x - self.size[0]/2 < 0:
            self.pos.x = self.size[0]/2
            self.velocity.x = 0
        if self.pos.x + self.size[0]/2 > tilemap.width * tilemap.tile_size:
            self.pos.x = tilemap.width * tilemap.tile_size - self.size[0]/2
            self.velocity.x = 0

        if self.pos.y - self.size[1]/2 < 0:
            self.pos.y = self.size[1]/2
            self.velocity.y = 0

        if self.pos.y + self.size[1]/2 > tilemap.height * tilemap.tile_size:
            self.pos.y = tilemap.height * tilemap.tile_size - self.size[1]/2
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
