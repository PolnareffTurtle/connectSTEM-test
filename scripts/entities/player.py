import pygame
from scripts.entities.entities import Entity
from scripts.enums import WeaponType,GameState
from scripts.weapon import Gun
from scripts.weaponmanager import WeaponManager

class Player(Entity):
    
    image_key = 'player'
    range = 50

    def __init__(self,scene,pos):
        super().__init__(scene, pos)
        self.speed = 200
        self.max_health = 100
        self.weapon_manager = WeaponManager(self)
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


        self.weapon_manager.update(dt)
        keys = pygame.key.get_pressed()
        self.weapon_manager.handle_input(keys, self.scene.EnemyList)
        if self.weapon_manager.active_weapon_type == WeaponType.ROTATE:
            self.weapon_manager.use_weapon(self.scene.EnemyList)
        
        for coin in self.scene.coins:
            if not coin.collected and self.aabb_collide(coin.rect()):
                coin.collect()

        self.weapon.update(dt)
        self.weapon.handle_input(self, targets=getattr(self.scene, "EnemyList", []))
        
        super().update(dt)
    
    def handle_event(self, event):
        self.weapon_manager.handle_event(event)
    
    def render(self, screen, offset):
        self.weapon_manager.render_weapon_visual(screen, offset)

        super().render(screen, offset)



        weapon = getattr(self.weapon_manager, "active_weapon", None)
        if weapon is None and hasattr(self.weapon_manager, "get_active_weapon"):
            weapon = self.weapon_manager.get_active_weapon()
        if weapon is not None:
            if hasattr(weapon, "draw_orbit_aim_indicator"):
                weapon.draw_orbit_aim_indicator(screen, self, length=14.0, radius=45.0)
            elif hasattr(weapon, "draw_aim_indicator"):
                weapon.draw_aim_indicator(screen, self, length=18.0, radius=50.0)


        if hasattr(self, "weapon") and self.weapon is not None:
            if hasattr(self.weapon, "draw_orbit_aim_indicator"):
                self.weapon.draw_orbit_aim_indicator(screen, self, length=14.0, radius=45.0)
            elif hasattr(self.weapon, "draw_aim_indicator"):
                self.weapon.draw_aim_indicator(screen, self, length=18.0, radius=50.0)
