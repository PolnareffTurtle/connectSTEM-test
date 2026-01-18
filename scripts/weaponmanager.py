import pygame
from scripts.weapon import CircleWeapon, RotateWeapon
from scripts.enums import WeaponType
import math

class WeaponManager:
    def __init__(self, player):
        self.player = player
        
        self.circle_weapon = CircleWeapon(
            attack_power=10,
            attack_speed=1/1.5,
            attack_radius=50
        )
        
        self.rotate_weapon = RotateWeapon(
            attack_power=5,
            attack_speed=4,
            radius=40,
            rotation_speed=480
        )
        
        self.weapons = {
            WeaponType.CIRCLE: self.circle_weapon,
            WeaponType.ROTATE: self.rotate_weapon
        }
        self.active_weapon_type = WeaponType.CIRCLE
        self.active_weapon = self.circle_weapon
    
    def switch_weapon(self):
        if self.active_weapon_type == WeaponType.CIRCLE:
            self.active_weapon_type = WeaponType.ROTATE
            self.active_weapon = self.rotate_weapon
        else:
            self.active_weapon_type = WeaponType.CIRCLE
            self.active_weapon = self.circle_weapon
    
    def use_weapon(self, targets):
        if self.active_weapon_type == WeaponType.CIRCLE:
            self.active_weapon.use(self.player, targets=targets)
        elif self.active_weapon_type == WeaponType.ROTATE:
            self.active_weapon.attack(self.player, targets=targets)
    
    def update(self, dt):
        self.circle_weapon.update(dt)
        self.rotate_weapon.update(dt)
    
    def handle_input(self, keys, targets):
        if keys[pygame.K_SPACE] and self.active_weapon_type == WeaponType.CIRCLE:
            self.use_weapon(targets)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.switch_weapon()

    def render_weapon_visual(self, screen, offset=(0, 0)):
        if self.active_weapon_type == WeaponType.CIRCLE:
            pygame.draw.circle(
                screen,
                (173, 216, 230),
                (int(self.player.pos.x - offset[0]), int(self.player.pos.y - offset[1])),
                self.circle_weapon.attack_radius,
                1
            )

            if self.circle_weapon.last_attack and self.circle_weapon.last_attack + 500 > pygame.time.get_ticks():
                surface = pygame.Surface((self.circle_weapon.attack_radius*2, self.circle_weapon.attack_radius*2), pygame.SRCALPHA)
                alpha = 200 - int(200 * (pygame.time.get_ticks() - self.circle_weapon.last_attack) / 500)
                pygame.draw.circle(surface, (0, 100, 255, alpha),
                                   (self.circle_weapon.attack_radius, self.circle_weapon.attack_radius), 
                                   self.circle_weapon.attack_radius)
                screen.blit(surface, (self.player.pos.x - offset[0] - self.circle_weapon.attack_radius, 
                                     self.player.pos.y - offset[1] - self.circle_weapon.attack_radius))
        
        elif self.active_weapon_type == WeaponType.ROTATE:
            weapon_x = self.player.pos.x + math.cos(math.radians(self.rotate_weapon.angle)) * self.rotate_weapon.radius
            weapon_y = self.player.pos.y + math.sin(math.radians(self.rotate_weapon.angle)) * self.rotate_weapon.radius
            
            center = (int(self.player.pos.x - offset[0]), int(self.player.pos.y - offset[1]))
            blade_pos = (int(weapon_x - offset[0]), int(weapon_y - offset[1]))
            
            pygame.draw.circle(screen, (128, 128, 128), blade_pos, 5)
            pygame.draw.line(screen, (150, 150, 150), center, blade_pos, 2)