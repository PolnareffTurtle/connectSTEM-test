import pygame
from scripts.scene import Scene
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.economy import Coin
from scripts.enemy import CircleEnemy, LungeEnemy, Enemy, RotateEnemy
from random import choice
from scripts.enums import GameState
from scripts.utils import Text

class GameplayScene(Scene):

    gamestate = GameState.GAMEPLAY

    def __init__(self, game):
        super().__init__(game)
        self.player = Player(self, (0,0))
        self.movement = [[0,0],[0,0]]  # [[left,right],[up,down]]
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
                    self.EnemyList.append(RotateEnemy(self, spawn['pos']))
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
        self.offset = self.player.pos - pygame.math.Vector2(self.game.display.get_size()) / 2

        self.wave = 1
        self.EnemyList = Enemy.create_wave(self, wave_number = self.wave, count = 3)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT,pygame.K_a]:
                    self.movement[0][0] = 1
                if event.key in [pygame.K_RIGHT,pygame.K_d]:
                    self.movement[0][1] = 1
                if event.key in [pygame.K_UP,pygame.K_w]:
                    self.movement[1][0] = 1
                if event.key in [pygame.K_DOWN,pygame.K_s]:
                    self.movement[1][1] = 1
                
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT,pygame.K_a]:
                    self.movement[0][0] = 0
                if event.key in [pygame.K_RIGHT,pygame.K_d]:
                    self.movement[0][1] = 0
                if event.key in [pygame.K_UP,pygame.K_w]:
                    self.movement[1][0] = 0
                if event.key in [pygame.K_DOWN,pygame.K_s]:
                    self.movement[1][1] = 0

    def update(self, dt):
        net_movement = (self.movement[0][1]-self.movement[0][0],self.movement[1][1]-self.movement[1][0])
        self.player.update(net_movement,dt)
        self.offset = self.player.pos - pygame.math.Vector2(self.game.display.get_size()) / 2
        self.render_offset = tuple(map(int,self.offset))
        for enemy in self.EnemyList: 
            if enemy.pos.distance_to(self.player.pos) < 50:
                enemy.health = 0
            enemy.update(dt)
        for coin in self.coins:
            if not coin.collected and self.player.aabb_collide(coin.rect()):
                coin.collect()
        #wave progression
        if not self.EnemyList:
            self.wave += 1
            self.EnemyList = Enemy.create_wave(self, wave_number = self.wave)
        
    def render(self, screen):
        screen.fill('aquamarine')
        self.tilemap.render(screen,offset=self.render_offset)
        self.player.render(screen,offset=self.render_offset)
        for coin in self.coins:
            coin.render(screen,offset=self.render_offset)  # draw uncollected coins
        for enemy in self.EnemyList:
            enemy.render(screen,offset=self.render_offset)
        text_surf = Text(f'Currency: {self.game.wallet.balance}    Wave: {self.wave}',10,color='black')
        text_surf.render(screen,(5,5))
