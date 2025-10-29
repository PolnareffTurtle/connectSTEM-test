import pygame
from sys import exit
from scripts.utils import load_image,load_images,spritesheet_to_surf_list
from scripts.enemy import Enemy, CircleEnemy, LungeEnemy
from scripts.player import Player
from scripts.enums import GameState
from scripts.economy import Wallet, Coin
from scripts.tilemap import Tilemap
from random import choice
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
            'coin': load_image('coin.png',alpha=True),
        }

        #economy setup
        self.wallet = Wallet()  # create player wallet


    def running(self):
        self.player = Player(self, (0,0))
        movement = [[0,0],[0,0]]  # [[left,right],[up,down]]
        self.EnemyList = []
        self.tilemap = Tilemap(self,map=0)
        self.coins = [  # example coin placements (you can adjust)
            Coin(self, (60, 60), value=5),
            Coin(self, (200, 120), value=10)
        ]
        ### SPAWN ENTITIES FROM TILEMAP ###
        for spawn in self.tilemap.spawns:
            if spawn['entity'] == 'enemy':
                if spawn.get('subclass') == 'circle':
                    self.EnemyList.append(CircleEnemy(self, spawn['pos']))
                elif spawn.get('subclass') == 'lunge':
                    self.EnemyList.append(LungeEnemy(self, spawn['pos']))
                elif spawn.get('subclass') == 'random':
                    EnemyClass = choice([CircleEnemy, LungeEnemy])
                    self.EnemyList.append(EnemyClass(self, spawn['pos']))
                else:
                    self.EnemyList.append(Enemy(self, spawn['pos']))
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
            for enemy in self.EnemyList:
                if enemy.pos.distance_to(self.player.pos) < 50 and enemy.health > 0:
                    enemy.health = 0  # instant kill for testing
                enemy.update(dt)
                
            ### RENDERING ###
            self.display.fill('aquamarine')
            self.tilemap.render(self.display,offset=render_offset)
            
            self.player.render(self.display,offset=render_offset)

            #coin collection logic
            for coin in self.coins:
                if not coin.collected and self.player.aabb_collide(coin.rect()):
                    coin.collect()

            #ender everything
            for coin in self.coins:
                coin.render(self.display,offset=render_offset)  # draw uncollected coins

            for enemy in self.EnemyList:
                enemy.render(self.display,offset=render_offset)

            """for enemy in self.EnemyList:
                if enemy.alive and abs(enemy.pos[0] - self.player.pos[0]) < 10 and abs(
                        enemy.pos[1] - self.player.pos[1]) < 10:
                    enemy.die()"""

            #render wallet bal
            """font = pygame.font.SysFont(None, 24)
            text = font.render(f"Coins: {self.wallet.balance}", True, (0, 0, 0))
            self.display.blit(text, (5, 5))"""

            self.clock.tick(60)
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))

            text_surf = pygame.font.Font(None, 30).render(f'Currency: {self.wallet.balance}',True,'black')
            self.screen.blit(text_surf,(10,10))
            pygame.display.update()

    def run(self):
        while True:
            if self.gamemode == GameState.GAME_RUNNING:
                self.running()

if __name__ == '__main__':
    game = Game()
    game.run()
