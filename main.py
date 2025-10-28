import pygame
from sys import exit
from scripts.utils import load_image,load_images
from scripts.enemy import Enemy
from scripts.player import Player
from scripts.enums import GameState
from scripts.economy import Wallet, Coin


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
            'coin': load_image('coin.jpg', alpha=True, scale = .1)
        }

        #economy setup
        self.wallet = Wallet()  # create player wallet
        self.coins = [  # example coin placements (you can adjust)
            Coin(self, (60, 60), value=5),
            Coin(self, (200, 120), value=10)
        ]

    def running(self):
        # place player at the center of the internal display (not the scaled window)
        self.player = Player(self, (self.display.get_width() // 2, self.display.get_height() // 2))
        movement = [[0,0],[0,0]]  # [[left,right],[up,down]]
        EnemyList = [Enemy(self, (100,100)),Enemy(self, (200,150)),Enemy(self, (150,50))]
        self.coins = []#store-dropped coins

        while self.gamemode == GameState.GAME_RUNNING:
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

            self.display.fill('aquamarine')
            self.player.update([movement[0][1]-movement[0][0],movement[1][1]-movement[1][0]])
            self.player.render(self.display)

            #coin collection logic
            for coin in self.coins:
                if not coin.collected and self.player.rect.colliderect(coin.rect):
                    coin.collect()

            #ender everything
            for coin in self.coins:
                coin.render(self.display)  # draw uncollected coins

            for enemy in EnemyList:
                enemy.render(self.display)

            for enemy in EnemyList:
                if enemy.alive and abs(enemy.pos[0] - self.player.pos[0]) < 10 and abs(
                        enemy.pos[1] - self.player.pos[1]) < 10:
                    enemy.die()

            #render wallet bal
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"Coins: {self.wallet.balance}", True, (0, 0, 0))
            self.display.blit(text, (5, 5))

            self.clock.tick(60)
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

    def run(self):
        while True:
            if self.gamemode == GameState.GAME_RUNNING:
                self.running()

if __name__ == '__main__':
    game = Game()
    game.run()

