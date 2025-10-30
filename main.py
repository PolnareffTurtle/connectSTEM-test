import pygame
from sys import exit
from scripts.utils import load_image,load_images,spritesheet_to_surf_list
from scripts.enums import GameState
from scripts.economy import Wallet
from scripts.gameplay_scene import GameplayScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.display = pygame.Surface((320,180))
        self.clock = pygame.time.Clock()
        self.gamestate = GameState.GAMEPLAY
        self.wallet = Wallet()  # create player wallet
        self.assets = {
            'player': load_image('player.png',alpha=True),
            'enemy': load_image('enemy.png',alpha=True),
            'tiles': spritesheet_to_surf_list(load_image('spritesheet.png',alpha=True),16,16,alpha=True,scale=1),
            'coin': load_image('coin.png',alpha=True),
        }
        self.scene = GameplayScene(self)

    def running(self):
        while self.gamestate == self.scene.gamestate:

            dt = self.clock.tick(60) / 1000

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.scene.handle_events(events)
            self.scene.update(dt)
            self.scene.render(self.display)

            self.clock.tick(60)
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

    def run(self):
        while True:
            if self.gamestate == GameState.GAMEPLAY:
                self.running()

if __name__ == '__main__':
    game = Game()
    game.run()
