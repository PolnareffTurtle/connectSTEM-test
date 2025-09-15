import pygame
from sys import exit


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.clock = pygame.time.Clock()
        self.gamemode = 'running'

    def running(self):
        while self.gamemode == 'running':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill('aquamarine')

            self.clock.tick(60)
            pygame.display.update()

    def run(self):
        while True:
            if self.gamemode == 'running':
                self.running()

if __name__ == '__main__':
    game = Game()
    game.run()

