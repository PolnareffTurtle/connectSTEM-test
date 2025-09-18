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
