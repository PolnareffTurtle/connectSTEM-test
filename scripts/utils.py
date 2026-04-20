import pygame
import os
from random import randint

BASE_IMG_PATH = 'assets/images/'

def load_image(path,alpha=False,scale=1):
    if alpha:
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
        img = pygame.transform.scale_by(img,scale)
        return img
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    img = pygame.transform.scale_by(img,scale)
    return img

def load_images(path,alpha=False,scale=1):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if img_name == '.DS_Store':
            continue
        images.append(load_image(path + '/' + img_name, alpha, scale))
    return images

def spritesheet_to_surf_list(spritesheet, sprite_w, sprite_h, alpha=False, scale=1):
    sheet_w, sheet_h = spritesheet.get_size()
    surf_list = []
    for y in range(0, sheet_h, sprite_h):
        for x in range(0, sheet_w, sprite_w):
            surf = pygame.Surface((sprite_w, sprite_h))
            if alpha:
                surf = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)
            surf.blit(spritesheet, (0, 0), (x, y, sprite_w, sprite_h))
            if not alpha:
                surf.set_colorkey((0, 0, 0))
            if scale != 1:
                surf = pygame.transform.scale_by(surf, scale)
            surf_list.append(surf)
    return surf_list


class Animation:
    def __init__(self, load_images_func, animations: dict[str, str], frame_duration: float = 0.12, loop: bool = True):
        self.frame_duration = frame_duration
        self.loop = loop
        self.timer = 0.0
        self.frame_index = 0
        self.current_animation = None
        self.animations: dict[str, list[pygame.Surface]] = {}

        for name, folder in animations.items():
            frames = load_images_func(folder)
            if isinstance(frames, pygame.Surface):
                frames = [frames]
            self.animations[name] = list(frames) if frames else []

        if self.animations:
            self.current_animation = next(iter(self.animations))

    def set_animation(self, name: str, reset: bool = False):
        if name not in self.animations:
            return
        if self.current_animation != name or reset:
            self.current_animation = name
            self.frame_index = 0
            self.timer = 0.0

    def update(self, dt: float):
        frames = self.get_current_frames()
        if len(frames) <= 1:
            return

        self.timer += dt
        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.frame_index += 1

            if self.frame_index >= len(frames):
                if self.loop:
                    self.frame_index = 0
                else:
                    self.frame_index = len(frames) - 1

    def get_current_frames(self) -> list[pygame.Surface]:
        if self.current_animation is None:
            return []
        return self.animations.get(self.current_animation, [])

    def get_current_frame(self) -> pygame.Surface | None:
        frames = self.get_current_frames()
        if not frames:
            return None
        self.frame_index = max(0, min(self.frame_index, len(frames) - 1))
        return frames[self.frame_index]


class Text:
    def __init__(self, text, font_size=20, font_path = 'assets/fonts/pixel.ttf', color=(255,255,255)):
        self.font = pygame.font.Font(font_path, font_size)
        self.color = color
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)

    def render(self, screen, **kwargs):
        rect = self.surface.get_rect(**kwargs)
        screen.blit(self.surface, rect)
