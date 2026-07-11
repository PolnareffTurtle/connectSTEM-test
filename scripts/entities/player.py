import pygame
from scripts.entities.entities import Entity
from scripts.enums import WeaponType,GameState
from scripts.weaponmanager import WeaponManager
from scripts.utils import Animation

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
        load_images = getattr(self.scene.game, "load_images", None)
        if callable(load_images):
            # combining pictures
            walk_frames = []
            for folder in ["pwalk", "pwalk1", "pwalk2"]:
                frames = load_images(folder)
                if isinstance(frames, pygame.Surface):
                    frames = [frames]
                walk_frames.extend(frames or [])

            idle_frames = []
            for folder in ["pstand", "pstand2"]:
                frames = load_images(folder)
                if isinstance(frames, pygame.Surface):
                    frames = [frames]
                idle_frames.extend(frames or [])

            self.animation = Animation(
                load_images,
                {
                    "idle": "pstand",  # placeholder (we override below)
                    "walk": "pwalk",
                },
                frame_duration=0.15,
            )

            self.animation.animations["idle"] = idle_frames
            self.animation.animations["walk"] = walk_frames
        else:
            self.animation = None

    def update(self,movement: tuple[int,int],dt):
        self.set_velocity(pygame.math.Vector2(movement))
        if self.velocity.magnitude() != 0:
            self.velocity.scale_to_length(self.speed)

        if self.animation is not None:
            if movement != (0, 0):
                self.animation.set_animation("walk")
            else:
                self.animation.set_animation("idle")

            self.animation.update(dt)
            frame = self.animation.get_current_frame()
            if frame:
                self.image = frame

        if self.health <= 0:
            self.scene.game.change_scene(GameState.DEATH)
            return

        self.weapon_manager.update(dt)
        self.weapon_manager.handle_input(self.scene.EnemyList)

        for coin in self.scene.coins:
            if not coin.collected and self.aabb_collide(coin.rect()):
                coin.collect()

        super().update(dt)
    
    def handle_event(self, event):
        self.weapon_manager.handle_event(event)
    
    def render(self, screen, offset):
        self.weapon_manager.render_weapon_visual(screen, offset)

        super().render(screen, offset)

        weapon = self.weapon_manager.active_weapon
        if weapon is not None and weapon.type == WeaponType.GUN:
            weapon.draw_orbit_aim_indicator(screen, self, length=14.0, radius=45.0)
