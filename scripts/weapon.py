import math
import pygame
from scripts.enums import WeaponType
import random
from scripts.projectile import Projectile

# add a bullet image
class Bullet(Projectile):
    image_key = 'coin'  # change this to a gun image, using coin for now

    def __init__(self, scene, pos, velocity: pygame.math.Vector2, damage: int = 1, targets: list = None):
        super().__init__(scene, pos, velocity)
        self.damage = damage
        self.targets = targets or []

    def update(self, dt):
        super().update(dt)

        if not hasattr(self, "scene") or self.scene is None:
            return

        for target in self.targets:
            if target is None or not hasattr(target, "health"):
                continue

            rect = None
            if hasattr(target, "rect") and callable(target.rect):
                rect = target.rect()
            elif hasattr(target, "aabb"):
                rect = target.aabb

            if rect is None:
                continue

            if self.aabb_collide(rect):
                target.health -= self.damage
                target.health = max(0, target.health)

                # Remove bullet after hit
                if hasattr(self.scene, "remove_projectile"):
                    self.scene.remove_projectile(self)
                elif hasattr(self.scene, "projectiles") and self in self.scene.projectiles:
                    self.scene.projectiles.remove(self)
                elif hasattr(self.scene, "entities") and self in self.scene.entities:
                    self.scene.entities.remove(self)
                break


class Weapon:
    type = None

    def __init__(self,attack_power: int = 1,attack_speed: float = 1):
        self.attack_power = attack_power
        self.attack_speed = attack_speed
        self.cooldown = 0
        self.last_attack = None

    def update(self, delta_time: float):
        if self.cooldown > 0:
            self.cooldown -= delta_time * random.uniform(0.8,1.2)
        if self.cooldown < 0:
            self.cooldown = 0

    def use(self, user, direction: pygame.Vector2 = None, targets: list = []):
        if self.cooldown <= 0:
            self.cooldown = 1 / self.attack_speed
            self.last_attack = pygame.time.get_ticks()
            self.attack(user, direction, targets)

    def handle_input(self, user, direction=None, targets: list = []):
        mouse_buttons = pygame.mouse.get_pressed()
        if not mouse_buttons[0]:
            return

        # convert the mouse position of the screen to the actual game position
        mx, my = pygame.mouse.get_pos()

        scene = getattr(user, "scene", None)
        if scene is None:
            return

        sx, sy = scene.game.scale
        mx /= sx
        my /= sy

        ro = getattr(scene, "render_offset", (0, 0))
        world_mouse = pygame.Vector2(mx + ro[0], my + ro[1])

        direction_vec = world_mouse - user.pos
        if direction_vec.length_squared() != 0:
            direction_vec = direction_vec.normalize()

        # CircleWeapon doesn't need direction, everything else does
        if isinstance(self, CircleWeapon):
            self.use(user, None, targets)
        else:
            self.use(user, direction_vec, targets)

    def attack(self, user, direction=None, targets: list = []):
        for target in targets:
            target.health -= self.attack_power
            target.health = max(0, target.health)

class CircleWeapon(Weapon):
    type = WeaponType.CIRCLE

    def __init__(self, attack_power, attack_speed, attack_radius=25):
        super().__init__(attack_power, attack_speed)
        self.attack_radius = attack_radius
        self.last_circle_attack = 0

    def attack(self, user, direction=None, targets: list = []):
        in_range = []
        for target in targets:
            if self.attack_radius >= user.pos.distance_to(target.pos):
                in_range.append(target)
        super().attack(user, targets=in_range)
    
    def render(self,screen,user,offset=(0,0)):
        pygame.draw.circle(
            screen,
            (173, 216, 230),
            (int(user.pos.x - offset[0]), int(user.pos.y - offset[1])),
            self.attack_radius,
            1
        )
        if self.last_attack and self.last_attack + 500 >pygame.time.get_ticks():
            surface = pygame.Surface((self.attack_radius*2, self.attack_radius*2),pygame.SRCALPHA)
            alpha = 200 - int(200 * (pygame.time.get_ticks() - self.last_attack)/500)
            pygame.draw.circle(surface, (0,100,255,alpha),
                               (self.attack_radius,self.attack_radius), 
                               self.attack_radius)
            screen.blit(surface, (user.pos.x - offset[0]-self.attack_radius, 
                                 user.pos.y - offset[1]-self.attack_radius))


class LungeWeapon(Weapon):
    type = WeaponType.LUNGE

    def __init__(self, attack_power,attack_speed):
        super().__init__(attack_power,attack_speed)

    def attack(self, user, direction, targets: list = []):
        user.velocity = direction * self.attack_power

class RotateWeapon(Weapon):
    type = WeaponType.ROTATE

    def __init__(self,attack_power,attack_speed,radius = 40,rotation_speed = 180):
        super().__init__(attack_power,attack_speed)
        self.radius = radius
        self.rotation_speed = rotation_speed
        self.angle = 0
        self.last_attack = 0

    def update(self, delta_time: float):
        super().update(delta_time)
        self.angle = (self.angle + self.rotation_speed * delta_time) % 360


    def use(self, user,direction: pygame.Vector2 = None,targets: list = []):
        self.attack(user, targets)

    def attack(self,user,targets: list = []):
        # translate to coords
        weapon_pos = pygame.Vector2(user.pos.x + math.cos(math.radians(self.angle)) * self.radius, user.pos.y + math.sin(math.radians(self.angle)) * self.radius)

        for target in targets:
            if target.pos.distance_to(weapon_pos) <= 15: # need better collision detection
                now = pygame.time.get_ticks()

                if now - self.last_attack > 250: # hard coded as well
                    target.health -= self.attack_power
                    target.health = max(0, target.health)
                    self.last_attack = now
    def render(self, screen, user, offset=(0, 0)):
        weapon_x = user.pos.x + math.cos(math.radians(self.angle)) * self.radius
        weapon_y = user.pos.y + math.sin(math.radians(self.angle)) * self.radius
        center = (int(user.pos.x - offset[0]), int(user.pos.y - offset[1]))
        blade_pos = (int(weapon_x - offset[0]), int(weapon_y - offset[1]))
        pygame.draw.circle(screen, (128, 128, 128), blade_pos, 5)
        pygame.draw.line(screen, (150, 150, 150), center, blade_pos, 2)

class Gun(Weapon):


    type = getattr(enums.WeaponType, "GUN", None)

    def __init__(self, attack_speed: float = 5, attack_power: int = 1, bullet_speed: float = 600.0):
        super().__init__(attack_power=attack_power, attack_speed=attack_speed)
        self.bullet_speed = bullet_speed

    def attack(self, user, direction: pygame.Vector2 = None, targets: list = []):
        if direction is None or direction.length_squared() == 0:
            print('shot')
            return

        direction = direction.normalize()
        spawn_pos = (user.pos.x, user.pos.y)
        velocity = direction * self.bullet_speed

        bullet = Bullet(user.scene, spawn_pos, velocity, damage=self.attack_power, targets=targets)

        scene = user.scene
        if hasattr(scene, "add_projectile") and callable(scene.add_projectile):
            scene.add_projectile(bullet)
        elif hasattr(scene, "projectiles"):
            scene.projectiles.append(bullet)
        elif hasattr(scene, "entities"):
            scene.entities.append(bullet)
