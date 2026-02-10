import pygame
from scripts.weapon import CircleWeapon, RotateWeapon
from scripts.enums import WeaponType

class WeaponManager:
    def __init__(self,player):
        self.player = player

        self.weapons=[
            CircleWeapon(attack_power=10,attack_speed=1/1.5, attack_radius=50),
            RotateWeapon(attack_power=5,attack_speed=4,radius=40,rotation_speed=480),
        ]
        
        self.active_index = 0
        self.active_weapon = self.weapons[self.active_index]
    

    def switch_weapon(self):
        self.active_index = (self.active_index+1)%len(self.weapons)
        self.active_weapon = self.weapons[self.active_index]
    
    def use_weapon(self, targets):
        self.active_weapon.use(self.player,targets=targets)
    
    def needs_continuous_attack(self):
        return self.active_weapon.type ==WeaponType.ROTATE
    
    def update(self, dt):
        for weapon in self.weapons:
            weapon.update(dt)

    def handle_input(self, keys, targets):
        if keys[pygame.K_SPACE]:
            self.use_weapon(targets)
    
    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.switch_weapon()

    def render_weapon_visual(self,screen,offset=(0, 0)):
        if hasattr(self.active_weapon,'render'):
            self.active_weapon.render(screen,self.player,offset)