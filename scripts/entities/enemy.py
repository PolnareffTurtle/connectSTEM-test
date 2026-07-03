import math

import pygame
from scripts.entities.entities import Entity
from scripts.enums import WeaponType
from scripts.weapon import Weapon, CircleWeapon, LungeWeapon, RotateWeapon
import random
from scripts.item import Coin
from scripts.utils import Animation
from random import randint,choice

class Enemy(Entity):
    image_key = 'enemy'
    range = 100
    value = 1

    def __init__(self,scene, pos=None, target:Entity=None, max_health: int = 100, attack: int = 5, level: int = 1):
        if not pos:
            pos = (random.randint(10, scene.tilemap.width*scene.tilemap.tile_size-10),
                   random.randint(10, scene.tilemap.height*scene.tilemap.tile_size-10))

        super().__init__(scene, pos)
        self.set_friction(200)
        self.target = target if target != None else scene.player

        self.max_health = max_health
        self.health = max_health
        self.attack = attack
        self.level = level

        self.idle_animation_folders = ["cstand1", "cstand2"]
        self.walk_animation_folders = ["cwalk"]
        self.attack_animation_folders = ["cattack"]
        self.shoot_animation_folders = ["cshoot"]
        self.animation = self._create_animation()
        self.attack_animation_timer = 0.0
        self.attack_animation_duration = 0.7
        self.attack_effect_frame = None
        self.attack_effect_angle = 0

    def _load_animation_frames(self, folders):
        load_images = getattr(self.scene.game, "load_images", None)
        assets = getattr(self.scene.game, "assets", {})
        frames = []

        for folder in folders:
            loaded = assets.get(folder, [])

            if not loaded and callable(load_images):
                try:
                    loaded = load_images(folder, alpha=True)
                except TypeError:
                    loaded = load_images(folder)
                except (FileNotFoundError, NotADirectoryError):
                    loaded = []

            if isinstance(loaded, pygame.Surface):
                loaded = [loaded]

            frames.extend(loaded or [])

        return frames

    def _create_animation(self):
        load_images = getattr(self.scene.game, "load_images", None)
        if not callable(load_images):
            return None

        animation = Animation(
            load_images,
            {},
            frame_duration=0.1,
        )

        animation.animations["idle"] = self._load_animation_frames(self.idle_animation_folders)
        animation.animations["walk"] = self._load_animation_frames(self.walk_animation_folders)
        animation.animations["attack"] = self._load_animation_frames(self.attack_animation_folders)
        animation.animations["shoot"] = self._load_animation_frames(self.shoot_animation_folders)
        animation.set_animation("idle")
        return animation

    def play_attack_animation(self, animation_name="attack"):
        if self.animation is None:
            return
        if animation_name not in self.animation.animations:
            return
        if not self.animation.animations[animation_name]:
            return
        self.attack_animation_timer = self.attack_animation_duration
        self.animation.set_animation(animation_name, reset=True)
        self.attack_effect_frame = self.animation.get_current_frame()

    def update_animation(self, dt):
        if self.animation is None:
            return

        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= dt
            self.animation.update(dt)
            self.attack_effect_frame = self.animation.get_current_frame()
            return

        self.attack_effect_frame = None
        if self.velocity.magnitude() > 1:
            self.animation.set_animation("walk")
        else:
            self.animation.set_animation("idle")

        self.animation.update(dt)
        frame = self.animation.get_current_frame()
        if frame:
            self.image = frame
    def render(self, screen, offset=(0, 0)):
        super().render(screen, offset)

        if self.attack_animation_timer > 0 and self.attack_effect_frame is not None:
            frame = pygame.transform.rotate(self.attack_effect_frame, self.attack_effect_angle)
            attack_rect = frame.get_rect(
                center=(int(self.pos.x - offset[0]), int(self.pos.y - offset[1]))
            )
            screen.blit(frame, attack_rect)

    def update(self, dt):
        super().update(dt)

        if self.health <= 0:
            if self in self.scene.EnemyList:
                self.on_death()
                self.scene.EnemyList.remove(self)
            return
        self.weapon.update(dt)
        self.update_animation(dt)

    def on_death(self):
        # drop a coin on death
        drop_pos = (self.pos[0] + randint(-3, 3), self.pos[1] + randint(-3, 3))
        coin = Coin(self.scene, drop_pos)
        if not hasattr(self.scene, 'coins'):
            self.scene.coins = []
        self.scene.coins.append(coin)

    @staticmethod
    def create_wave(scene, wave_number, count = None):
        if not count:
            count = int(min(3 + .8 * wave_number + .04 * wave_number ** 2, 28))
        enemies = [] #to create and return list of enemies per wave
        for i in range(count):
            # random spawn positions (across whole map rather than visible screen)
            pos = (randint(10, scene.tilemap.width * scene.tilemap.tile_size - 10),
                   randint(10, scene.tilemap.height * scene.tilemap.tile_size - 10))

            EnemyType = choice((CircleEnemy,LungeEnemy,RotateEnemy))
            enemies.append(EnemyType(scene, pos, level=wave_number))
        return enemies


class CircleEnemy(Enemy):

    def __init__(self,scene, pos=None, target:Entity=None, level: int = 1):
        # diff scaling for each enemy type
        attack = int((level - 1) * 0.5 + 10)
        max_health = 5 + (level - 1) * 2

        super().__init__(scene, pos, target, max_health=max_health, attack=attack, level=level)
        self.weapon = CircleWeapon(attack_power=attack, attack_speed=1, attack_radius=30)
        self.value = 1 + self.level // 2

    def update(self, dt):
        last_attack = self.weapon.last_attack
        self.weapon.use(self, targets=[self.target])
        if self.weapon.last_attack != last_attack:
            self.play_attack_animation("attack")
        super().update(dt)

    def render(self,screen,offset=(0,0)):

        # this is a pulsing circle to show the attack radius
        if self.weapon.last_attack and self.weapon.last_attack + 500 > pygame.time.get_ticks():
            # pygame is weird and requires surfaces for alpha
            surface = pygame.Surface((self.weapon.attack_radius*2,self.weapon.attack_radius*2),pygame.SRCALPHA)
            alpha = 200 - int(200 * (pygame.time.get_ticks() - self.weapon.last_attack) / 500)
            pygame.draw.circle(surface, (255,0,0,alpha),
                               (self.weapon.attack_radius,self.weapon.attack_radius),
                               self.weapon.attack_radius)
            screen.blit(surface, self.pos-offset-(self.weapon.attack_radius,self.weapon.attack_radius))
        super().render(screen,offset)


class LungeEnemy(Enemy):

    def __init__(self,scene, pos=None, target:Entity=None,  level: int = 1):
        attack = int((level - 1) * 5 + 10)
        max_health = 5 + (level - 1) * 2

        super().__init__(scene, pos, target, max_health=max_health, attack=attack, level=level)
        # not actually hurting player; attack power determines speed
        self.weapon = LungeWeapon(attack_power=attack, attack_speed=0.3)
        self.attack_animation_folders = ["sattack"]
        self.shoot_animation_folders = ["sshoot"]
        self.animation = self._create_animation()
        self.value = int(3 + self.level * 0.5)

    def update(self, dt):
        direction = self.target.pos - self.pos # pygame.Vector2
        if direction.magnitude() < self.range:
            if direction.magnitude() != 0:
                direction = direction.normalize()
            last_attack = self.weapon.last_attack
            self.weapon.use(self, direction=direction)
            if self.weapon.last_attack != last_attack:
                self.attack_effect_angle = direction.angle_to(pygame.Vector2(1, 0))
                self.play_attack_animation("attack")
                self.target.health -= self.attack
                self.target.health = max(0, self.target.health)
        super().update(dt)


class RotateEnemy(Enemy):

    def __init__(self, scene, pos = None, target: Entity = None,  level: int = 1):
        attack = int((level - 1) * 0.5 + 5)
        max_health = 5 + (level - 1) * 2

        super().__init__(scene, pos, target, max_health=max_health, attack=attack, level=level)
        self.weapon = RotateWeapon(attack_power = attack, attack_speed = 1.5, radius = 14, rotation_speed = 240)
        self.sword_frames = self._load_animation_frames(["sattack", "sshoot", "sidle"])
        self.sword_scale = 2.5
        self.sword_handle_offset = pygame.Vector2(0, -10)
        self.value = int(3 + level * 0.5)

    def update(self, dt):
        last_attack = self.weapon.last_attack
        self.weapon.attack(self, targets = [self.target])
        if self.weapon.last_attack != last_attack:
            self.play_attack_animation("shoot")
        super().update(dt)

    def render(self, screen, offset = (0, 0)):
        center = self.pos - offset
        orbit_angle = math.radians(self.weapon.angle)
        handle_end = pygame.Vector2(
            center.x + math.cos(orbit_angle) * self.weapon.radius,
            center.y + math.sin(orbit_angle) * self.weapon.radius
        )

        if self.sword_frames:
            frame_index = int(pygame.time.get_ticks() / 100) % len(self.sword_frames)
            sword_frame = self.sword_frames[frame_index]
            sword_frame = pygame.transform.scale_by(sword_frame, self.sword_scale)

            sword_angle = self.weapon.angle + 90
            rotated_sword = pygame.transform.rotate(sword_frame, -sword_angle)

            original_anchor = pygame.Vector2(
                sword_frame.get_width() / 2 + self.sword_handle_offset.x * self.sword_scale,
                sword_frame.get_height() / 2 + self.sword_handle_offset.y * self.sword_scale
            )
            original_center = pygame.Vector2(sword_frame.get_width() / 2, sword_frame.get_height() / 2)
            anchor_from_center = original_anchor - original_center
            rotated_anchor_from_center = anchor_from_center.rotate(sword_angle)

            sword_center = handle_end - rotated_anchor_from_center
            sword_rect = rotated_sword.get_rect(center=(int(sword_center.x), int(sword_center.y)))
            screen.blit(rotated_sword, sword_rect)
        else:
            pygame.draw.circle(screen, (255, 50, 50), (int(handle_end.x), int(handle_end.y)), 6)
            pygame.draw.line(screen, (255, 100, 100), handle_end, center, 2)

        super().render(screen, offset)
