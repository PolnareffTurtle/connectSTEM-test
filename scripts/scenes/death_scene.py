from scripts.scenes.scene import Scene
from scripts.utils import Text
from scripts.button import NavButton
from scripts.enums import GameState
import pygame

class DeathScene(Scene):
    def __init__(self,game):
        super().__init__(game)
        display_rect = self.game.display.get_rect()
        play_rect = pygame.Rect((0,0,60,20))
        play_rect.center = display_rect.centerx - 35, display_rect.centery + 30
        home_rect = pygame.Rect((0,0,60,20))
        home_rect.center = display_rect.centerx + 35,display_rect.centery+30

        button_font = pygame.font.Font('assets/fonts/pixel.ttf',10)
        self.buttons = [
            NavButton(play_rect,'Play Again',button_font,(100,100,100),(255,255,255),GameState.GAMEPLAY,border_radius=3,alt_color=(200,200,200)),
            NavButton(home_rect,'Quit',button_font,(100,100,100),(255,255,255),GameState.MAIN_MENU,border_radius=3,alt_color=(200,200,200))
        ]

    def handle_events(self,events):
        for event in events:
            for button in self.buttons:
                button.update(event,self.game)

    def update(self,dt):
        pass

    def render(self,screen):
        screen.fill((0,0,0))
        screen_rect = screen.get_rect()
        for button in self.buttons:
            button.draw(screen)
        Text('You died...',20,color=(255,0,0)).render(screen,center=screen_rect.center)
        
