import pygame
from scripts.entities.entities import Entity
from scripts.enums import WeaponType,GameState
from scripts.weaponmanager import WeaponManager

class Player(Entity):
    
    image_key = 'player'
    range = 50

    def __init__(self,scene,pos):
        super().__init__(scene, pos)
        self.speed = 200
        self.max_health = 100
        self.weapon_manager = WeaponManager(self)

    def update(self,movement: tuple[int,int],dt):
        self.set_velocity(pygame.math.Vector2(movement))
        if self.velocity.magnitude() != 0:
            self.velocity.scale_to_length(self.speed)

        if self.health <= 0:
            self.scene.game.change_scene(GameState.DEATH)
            return


        self.weapon_manager.update(dt)
        keys = pygame.key.get_pressed()
        self.weapon_manager.handle_input(keys, self.scene.EnemyList)
        if self.weapon_manager.active_weapon_type == WeaponType.ROTATE:
            self.weapon_manager.use_weapon(self.scene.EnemyList)
        
        for coin in self.scene.coins:
            if not coin.collected and self.aabb_collide(coin.rect()):
                coin.collect()
        
        super().update(dt)
    
    def handle_event(self, event):
        self.weapon_manager.handle_event(event)
    
    def render(self, screen, offset):
        self.weapon_manager.render_weapon_visual(screen, offset)
        super().render(screen, offset)