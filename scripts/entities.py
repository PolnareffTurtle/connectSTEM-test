import pygame

class Entity:
    def __init__(self,game,pos,image_key):
        self.image = game.assets[image_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.game = game
    
    def render(self,screen):
        screen.blit(self.image,self.rect)


class Player(Entity):
    def __init__(self,game,pos):
        super().__init__(game, pos, 'player')
        self.speed = 5

    def update(self,movement):
        self.rect.x += movement[0] * self.speed
        self.rect.y += movement[1] * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        # use the internal display surface for bounds checks (rendering is to `game.display`)
        display_w = self.game.display.get_width()
        display_h = self.game.display.get_height()
        if self.rect.right > display_w:
            self.rect.right = display_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > display_h:
            self.rect.bottom = display_h


    

class Enemy(Entity):
    def __init__(self,game,pos):
        super().__init__(game, pos, 'enemy')

