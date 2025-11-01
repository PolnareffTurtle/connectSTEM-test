import pygame
from scripts.enums import GameState

"""
all songs must be commercially licenced! below is where these songs are from:
reed_flutes.ogg, waltz_of_flowers.ogg, sugar_plum_fairy.ogg

Music: “[Track Title]” by Gregor Quendel / Classicals.de 
Source: https://www.classicals.de
"""

class Music:
    ROOT_PATH = 'assets/sounds/music/'
    gamestate_factory = {
        GameState.MAIN_MENU: ['waltz_of_flowers.ogg'],
        GameState.GAMEPLAY: ['reed_flutes.ogg'],
        GameState.DEATH: ['sugar_plum_fairy.ogg'],
        GameState.PAUSE: None,
    }
    queue = []
    NEXT = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(NEXT)

    @staticmethod
    def play(gamestate: GameState):
        if gamestate == GameState.PAUSE:
            return
        Music.queue = [Music.ROOT_PATH + path for path in Music.gamestate_factory[gamestate]]
        pygame.mixer.music.load(Music.queue[0])
        Music.queue.append(Music.queue.pop(0))
        pygame.mixer.music.play()
        
    @staticmethod
    def update(event, gamestate):
        if gamestate == GameState.PAUSE:
            pygame.mixer.music.set_volume(0.4)
        else:
            pygame.mixer.music.set_volume(1)
        if event.type == Music.NEXT:
            pygame.mixer.music.queue(Music.queue[0])
            Music.queue.append(Music.queue.pop(0))
