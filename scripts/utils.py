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

class Text:
    def __init__(self, text, font_size=20, font = None, color=(255,255,255)):
        self.font = pygame.font.Font('assets/fonts/pixel.ttf', font_size)
        self.color = color
        self.text = text
        self.image = self.font.render(self.text, True, self.color)

    def render(self, screen, pos):
        screen.blit(self.image, pos)
