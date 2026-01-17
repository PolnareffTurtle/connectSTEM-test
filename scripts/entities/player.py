import pygame
from scripts.entities.entities import Entity
from scripts.enums import WeaponType,GameState
from scripts.weapon import Gun

class Player(Entity):
    
    image_key = 'player'
    range = 50

    def __init__(self,scene,pos):
        super().__init__(scene, pos)
        self.speed = 200
        self.max_health = 100
        self.scene = scene
        self.pos = pygame.Vector2(pos)
        self.weapon = Gun(
            attack_speed=5,
            attack_power=1,
            bullet_speed=600,
        )

    def update(self,movement: tuple[int,int],dt):
        self.set_velocity(pygame.math.Vector2(movement))
        if self.velocity.magnitude() != 0:
            self.velocity.scale_to_length(self.speed)

        if self.health <= 0:
            self.scene.game.change_scene(GameState.DEATH)
            return

        
        for coin in self.scene.coins:
            if not coin.collected and self.aabb_collide(coin.rect()):
                coin.collect()
        
        # updates gun
        self.weapon.update(dt)
        self.weapon.handle_input(self, targets=getattr(self.scene, "EnemyList", []))
        super().update(dt)

    def render(self, screen, offset):
        # poison attack for now
        transparent_surf = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA)
        pygame.draw.circle(transparent_surf, (109, 122, 38,170), (self.range,self.range), self.range)
        screen.blit(transparent_surf, (self.pos.x - self.range - offset[0], self.pos.y - self.range - offset[1]))
        super().render(screen, offset)

