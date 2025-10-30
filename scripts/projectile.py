import pygame
from scripts.collide import Collide

class Projectile(Collide):
    
    image_key = 'projectile'

    def __init__(self, scene, pos: tuple[float,float], velocity: pygame.math.Vector2):
        super().__init__(scene, self.image_key, pos)
        self.set_velocity(velocity)

    def set_velocity(self, velocity: pygame.math.Vector2):
        self.velocity = velocity

    def check_wall_collisions(self, rects):
        for rect in rects:
            if self.aabb_collide(rect):
                self.wallBounceBehavior()
            
    def update(self, dt):
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

        tilemap = self.scene.tilemap
        physics_rects = tilemap.physics_rects_around(self.pos)

        self.check_wall_collisions(physics_rects)

    def wallBounceBehavior(self):
        # Default behavior: destroy the projectile
        self.scene.remove_projectile(self)
