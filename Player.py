import pygame

from enums import GameState

player_health = 100
horizontal_movement = [False, False]
vertical_movement = [False, False]

def game_running(self):
    while self.game_running == GameState.GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_a:
                    horizontal_movement[0] = True
                if event.key == pygame.K_d:
                    horizontal_movement[1] = True
                if event.key == pygame.K_w:
                    vertical_movement[0] = True
                if event.key == pygame.K_s:
                    vertical_movement[1] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    horizontal_movement[0] = False
                if event.key == pygame.K_d:
                    horizontal_movement[1] = False
                if event.key == pygame.K_w:
                    vertical_movement[0] = False
                if event.key == pygame.K_s:
                    vertical_movement[1] = False

