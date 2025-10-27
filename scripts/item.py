import pygame
from scripts.enums import ItemType
class Item():
    image_key = 'CoinSprite(TEMP)'
    type= ItemType.NONE
    def __init__(self, game, startPos, autoPickup: bool = True):
        self.autoPickup = autoPickup #if the item should be picked up automatically on contact
        self.image = game.assets[self.image_key]
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(startPos)
        self.game = game


    def render(self,screen,offset=(0,0)):
        rect = self.rect()
        screen.blit(self.image,(rect.x-offset[0],rect.y-offset[1]))

    def rect(self):
        return self.image.get_rect(center=(int(self.pos.x),int(self.pos.y)))
        