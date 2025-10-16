import pygame
from math import sqrt
from scripts.entities import Entity

class Player(Entity):
    def __init__(self,game,pos):
        super().__init__(game, pos, 'player')
        self.speed = 3
        self.max_health = 100
        self.health = 100

    def check_collisions(self,player_rect,rects,prev_movement):
        for rect in rects:
            if rect.colliderect(player_rect):
                if prev_movement[0] < 0:
                    player_rect.left = rect.right
                elif prev_movement[0] > 0:
                    player_rect.right = rect.left
                if prev_movement[1] < 0:
                    player_rect.top = rect.bottom
                elif prev_movement[1] > 0:
                    player_rect.bottom = rect.top
        self.pos[0] = player_rect.centerx
        self.pos[1] = player_rect.centery

    def update(self,movement,tilemap):
        player_rect = self.rect()
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        physics_rects = tilemap.physics_rects_around(self.pos)

        # normalize for speed moving diagonally 
        # check for collisions
        x_movement = movement[0] * self.speed
        y_movement = movement[1] * self.speed
        if movement[0] and movement[1]:
            player_rect.x += x_movement / sqrt(2)
            self.check_collisions(player_rect,physics_rects,[x_movement/sqrt(2),0])
            player_rect.y += y_movement / sqrt(2)
            self.check_collisions(player_rect,physics_rects,[0,y_movement/sqrt(2)])
        else:
            player_rect.x += x_movement
            self.check_collisions(player_rect,physics_rects,[x_movement,0])
            player_rect.y += y_movement
            self.check_collisions(player_rect,physics_rects,[0,y_movement])

        # check for bounds
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > tilemap.width * tilemap.tile_size:
            player_rect.right = tilemap.width * tilemap.tile_size
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > tilemap.height * tilemap.tile_size:
            player_rect.bottom = tilemap.height * tilemap.tile_size
        self.pos = [player_rect.centerx,player_rect.centery]
