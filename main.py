import pygame
from sys import exit

from scripts.scenes.options_menu_scene import OptionsMenuScene
from scripts.utils import load_image,load_images,spritesheet_to_surf_list
from scripts.enums import GameState
from scripts.scenes.gameplay_scene import GameplayScene
from scripts.scenes.main_menu_scene import MainMenuScene
from scripts.scenes.pause_scene import PauseScene
from scripts.scenes.death_scene import DeathScene
from scripts.scenes.scene import Scene
from scripts.music import Music
import asyncio

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.display = pygame.Surface((320,180))
        self.clock = pygame.time.Clock()
        self.assets = {
            'player': load_image('player.png',alpha=True),
            'enemy': load_image('enemy.png',alpha=True),
            'tiles': spritesheet_to_surf_list(load_image('spritesheet.png',alpha=True),16,16,alpha=True,scale=1),
            'coin': load_image('coin.png',alpha=True),
            #add a bullet asset here
        }
        self.scene_factories = {
            GameState.MAIN_MENU: MainMenuScene,
            GameState.GAMEPLAY: GameplayScene,
            GameState.PAUSE: PauseScene,
            GameState.DEATH: DeathScene,
            GameState.OPTIONS: OptionsMenuScene
        }
        self.scene = None
        self.scene_stack = [] # for pause/resume
        self.next_scene = GameState.MAIN_MENU
    
    @property
    def scale(self):
        return (self.screen.get_width()/self.display.get_width(), self.screen.get_height()/self.display.get_height())
    
    @property
    def gamestate(self):
        for state, cls in self.scene_factories.items():
            if isinstance(self.scene, cls):
                return state
        return None

    async def run_scene(self):
        while self.scene.running and self.next_scene is None:

            dt = self.clock.tick(60) / 1000

            events = pygame.event.get()
            for event in events:
                Music.update(event,self.gamestate)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.scene.handle_events(events)
            self.scene.update(dt)
            self.scene.render(self.display)

            self.clock.tick(60)
            await asyncio.sleep(0)
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

    def change_scene(self,scene_type: GameState):
        self.next_scene = scene_type

    async def run(self):
        SceneType = self.scene_factories[self.next_scene]
        self.next_scene = None
        self.scene = SceneType(self)
        Music.play(self.gamestate)
        while True:
            
            await self.run_scene()

            # if pause scene ends, go back to previous
            if not self.scene.running and self.scene_stack:
                self.scene = self.scene_stack.pop()
            # if another scene was requested
            elif self.next_scene:
                # if pausing, remember the current one
                if isinstance(self.scene, GameplayScene) and self.next_scene == GameState.PAUSE:
                    self.scene_stack.append(self.scene)
                SceneType = self.scene_factories[self.next_scene]
                self.scene = SceneType(self)
                Music.play(self.gamestate)
            else:
                raise Exception('Next Scene not found')

            self.next_scene = None
            
            await asyncio.sleep(0)
            
if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())
