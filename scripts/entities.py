import pygame
from scripts.weapon import Weapon

class Entity:
    def __init__(self,game,pos,image_key,atk=1,atk_spd=1):
        self.image = game.assets[image_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.game = game
        self.weapon = Weapon(atk,atk_spd)
        self.health = 100
        self.max_health = 100
        self.health_bar_height = 5

    def render(self,screen):
        screen.blit(self.image,self.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = self.rect.width
        bar_height = self.health_bar_height
        health_ratio = self.health / self.max_health
        green_width = int(bar_width * health_ratio)
        bar_x = self.rect.left
        bar_y = self.rect.top - bar_height - 2
        red_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        green_bar_rect = pygame.Rect(bar_x, bar_y, green_width, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), red_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), green_bar_rect)

    def attack(self):
        self.weapon.use()

    def take_damage(self, amount):
        self.health = (self.health - amount)
        self.health_bar_height = self.health_bar_height - 1
