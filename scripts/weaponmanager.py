import pygame
from scripts.weapon import CircleWeapon, RotateWeapon, Gun

class WeaponManager:
    def __init__(self,player):
        self.player = player

        self.weapons=[
            CircleWeapon(attack_power=10,attack_speed=1/1.5, attack_radius=50),
            RotateWeapon(attack_power=5,attack_speed=4,radius=40,rotation_speed=480),
            Gun(attack_speed=5, attack_power=1, bullet_speed=600),
        ]

        self.active_index = 0
        self.active_weapon = self.weapons[self.active_index]


    def switch_weapon(self):
        self.active_index = (self.active_index+1)%len(self.weapons)
        self.active_weapon = self.weapons[self.active_index]

    def update(self, dt):
        for weapon in self.weapons:
            weapon.update(dt)

    def handle_input(self, targets):
        if self.active_weapon.continuous:
            # continuous weapons (e.g. the rotating blade) attack every frame
            self.active_weapon.use(self.player, targets=targets)
        else:
            # otherwise left mouse fires the active weapon, aimed at the cursor
            self.active_weapon.handle_input(self.player, targets=targets)

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.switch_weapon()

    def render_weapon_visual(self,screen,offset=(0, 0)):
        if hasattr(self.active_weapon,'render'):
            self.active_weapon.render(screen,self.player,offset)