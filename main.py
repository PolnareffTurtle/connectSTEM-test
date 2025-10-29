import pygame
from sys import exit
from scripts.utils import load_image,load_images,spritesheet_to_surf_list
from scripts.enemy import Enemy, CircleEnemy, LungeEnemy
from scripts.player import Player
from scripts.enums import GameState
from scripts.tilemap import Tilemap
from random import choice
from scripts.coin import Coin;
class Game:
    currency = 0
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.display = pygame.Surface((320,180))
        self.clock = pygame.time.Clock()
        self.gamemode = GameState.GAME_RUNNING
        self.CoinList = [];
        self.assets = {
            'player': load_image('player.png',alpha=True),
            'enemy': load_image('enemy.png',alpha=True),
            'tiles': spritesheet_to_surf_list(load_image('spritesheet.png',alpha=True),16,16,alpha=True,scale=1),
            'CoinSprite(TEMP)': load_image('CoinSprite(TEMP).png',alpha=True),
        }

    def running(self):
        self.player = Player(self, (0,0))
        movement = [[0,0],[0,0]]  # [[left,right],[up,down]]
        EnemyList = []
        self.CoinList = [Coin(self, (200,200), value=5)];
        self.tilemap = Tilemap(self,map=0)

        ### SPAWN ENTITIES FROM TILEMAP ###
        for spawn in self.tilemap.spawns:
            if spawn['entity'] == 'enemy':
                if spawn.get('subclass') == 'circle':
                    EnemyList.append(CircleEnemy(self, spawn['pos']))
                elif spawn.get('subclass') == 'lunge':
                    EnemyList.append(LungeEnemy(self, spawn['pos']))
                elif spawn.get('subclass') == 'random':
                    EnemyClass = choice([CircleEnemy, LungeEnemy])
                    EnemyList.append(EnemyClass(self, spawn['pos']))
                else:
                    EnemyList.append(Enemy(self, spawn['pos']))
            elif spawn['entity'] == 'player':
                self.player.pos = pygame.math.Vector2(spawn['pos'])

        # this makes the player centered on the screen
        offset = self.player.pos - pygame.math.Vector2(self.display.get_size()) / 2
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
            offset = self.player.pos - pygame.math.Vector2(self.display.get_size()) / 2
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
            
            for coin in self.CoinList:
                coin.render(self.display,offset=render_offset)

            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))

            text_surf = pygame.font.Font(None, 30).render(f'Currency: {self.currency}',True,'black')
            self.screen.blit(text_surf,(10,10))
            pygame.display.update()

    def run(self):
        while True:
            if self.gamemode == GameState.GAME_RUNNING:
                self.running()

if __name__ == '__main__':
    game = Game()
    game.run()
