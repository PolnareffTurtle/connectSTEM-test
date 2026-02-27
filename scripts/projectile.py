import pygame
from scripts.collide import Collide

class Projectile(Collide):
    
    image_key = 'coin'

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

    def render(self, screen, offset=(0, 0)):
        # Draw using an asset that exists in Game.assets
        img = None
        if hasattr(self.scene, "game") and hasattr(self.scene.game, "assets"):
            img = self.scene.game.assets.get(self.image_key)

        if img is None:
            return

        screen.blit(img, (self.pos.x - offset[0], self.pos.y - offset[1]))

    def wallBounceBehavior(self):
        # Default behavior: destroy the projectile
        self.scene.remove_projectile(self)
