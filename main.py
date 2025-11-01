import pygame
from sys import exit
from scripts.utils import load_image,load_images,spritesheet_to_surf_list
from scripts.enums import GameState
from scripts.scenes.gameplay_scene import GameplayScene
from scripts.scenes.main_menu_scene import MainMenuScene
from scripts.scenes.pause_scene import PauseScene
from scripts.scenes.death_scene import DeathScene
from scripts.scenes.scene import Scene
from scripts.music import Music

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
        }
        self.scene_factories = {
            GameState.MAIN_MENU: MainMenuScene,
            GameState.GAMEPLAY: GameplayScene,
            GameState.PAUSE: PauseScene,
            GameState.DEATH: DeathScene
        }
    
    @property
    def scale(self):
        return (self.screen.get_width()/self.display.get_width(), self.screen.get_height()/self.display.get_height())
    
    @property
    def gamestate(self):
        for state, cls in self.scene_factories.items():
            if isinstance(self.scene, cls):
                return state
        return None

    def run_scene(self, scene_type: Scene):
        self.scene = scene_type(self)
        Music.play(self.gamestate)
        while self.scene.running:

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
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

    def change_scene(self,scene_type: GameState):
        prev = self.scene
        scene = self.scene_factories[scene_type]
        self.run_scene(scene)
        self.scene = prev # when run_scene finishes, return to the original scene


if __name__ == '__main__':
    game = Game()
    game.run_scene(MainMenuScene)
