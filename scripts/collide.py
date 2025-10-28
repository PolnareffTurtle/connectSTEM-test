import pygame
class collide:
    def __init__(self, game, image_key, pos: tuple[float,float]):
        self.image = game.assets[image_key]
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(pos)
        self.game = game

#draws the Object at its position with an optional offset
    def render(self,screen,offset=(0,0)):
        rect = self.rect()
        screen.blit(self.image,(rect.x-offset[0],rect.y-offset[1]))

#checks if the object collides with a given rectangle using AABB method, preserving float position
    def aabb_collide(self,rect: pygame.Rect) -> bool:
        return ( 
            self.pos.x - self.size[0]/2 < rect.right and
            self.pos.x + self.size[0]/2 > rect.left and
            self.pos.y - self.size[1]/2 < rect.bottom and
            self.pos.y + self.size[1]/2 > rect.top
        )

    def rect(self):
        return self.image.get_rect(center=(int(self.pos.x),int(self.pos.y)))
    
    def update(self, dt):
        pass