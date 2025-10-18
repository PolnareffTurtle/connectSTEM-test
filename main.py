import pygame
from sys import exit
from scripts.utils import load_image,load_images,spritesheet_to_surf_list
from scripts.enemy import Enemy
from scripts.player import Player
from scripts.enums import GameState
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.display = pygame.Surface((320,180))
        self.clock = pygame.time.Clock()
        self.gamemode = GameState.GAME_RUNNING
        self.assets = {
            'player': load_image('player.png',alpha=True),
            'enemy': load_image('enemy.png',alpha=True),
            'tiles': spritesheet_to_surf_list(load_image('spritesheet.png',alpha=True),16,16,alpha=True,scale=1),
        }

    def running(self):
        self.player = Player(self, (0,0))
        movement = [[0,0],[0,0]]  # [[left,right],[up,down]]
        EnemyList = [Enemy(self, (100,100)),Enemy(self, (200,150)),Enemy(self, (150,50))]
        self.tilemap = Tilemap(self,map=0)

        # this makes the player centered on the screen
        offset = [
            self.player.pos[0] - self.display.get_width() / 2, 
            self.player.pos[1] - self.display.get_height() / 2
            ]
        EnemyList = [Enemy(self, (100,100)),Enemy(self, (200,150)),Enemy(self, (150,50)), Enemy(self)]
        EnemyList = [Enemy(self,(100,100))]
        while self.gamemode == GameState.GAME_RUNNING:

            dt = self.clock.tick(60) / 1000

            ### INPUTS ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT,pygame.K_a]:
                        movement[0][0] = 1
                    if event.key in [pygame.K_RIGHT,pygame.K_d]:
                        movement[0][1] = 1
                    if event.key in [pygame.K_UP,pygame.K_w]:
                        movement[1][0] = 1
                    if event.key in [pygame.K_DOWN,pygame.K_s]:
                        movement[1][1] = 1
                    
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT,pygame.K_a]:
                        movement[0][0] = 0
                    if event.key in [pygame.K_RIGHT,pygame.K_d]:
                        movement[0][1] = 0
                    if event.key in [pygame.K_UP,pygame.K_w]:
                        movement[1][0] = 0
                    if event.key in [pygame.K_DOWN,pygame.K_s]:
                        movement[1][1] = 0

            # update player position with net_movment
            net_movement = (movement[0][1]-movement[0][0],movement[1][1]-movement[1][0])
            self.player.update(net_movement,dt)

            # rigid offset scrolling
            offset[0] = self.player.pos[0] - self.display.get_width() / 2
            offset[1] = self.player.pos[1] - self.display.get_height() / 2
            # integer render offset for pixel alignment
            render_offset = tuple(map(int,offset))

            ### UPDATES ###
            for enemy in EnemyList:
                enemy.update(dt)
                
            ### RENDERING ###
            self.display.fill('aquamarine')
            self.tilemap.render(self.display,offset=render_offset)
            
            self.player.render(self.display,offset=render_offset)
            for enemy in EnemyList:
                enemy.render(self.display,offset=render_offset)
            
            
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

    def run(self):
        while True:
            if self.gamemode == GameState.GAME_RUNNING:
                self.running()

if __name__ == '__main__':
    game = Game()
    game.run()

