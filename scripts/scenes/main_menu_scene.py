import pygame
from scripts.scenes.scene import Scene
from scripts.button import NavButton, Button
from scripts.enums import GameState
from scripts.utils import Text

class MainMenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        button_font = pygame.font.Font('assets/fonts/pixel.ttf',10)
        play_button_rect = pygame.Rect(0,0,50,20)
        option_button_rect = pygame.Rect(0,0,50,20)
        play_button_rect.center = game.display.get_width()//2,game.display.get_height()//2 + 40
        option_button_rect.center = game.display.get_width()//2,game.display.get_height()//2 + 65

        self.buttons = [
            NavButton(play_button_rect,'Play',button_font,(255,255,255,200),(0,0,0),GameState.GAMEPLAY,border_radius=3,alt_color=(200,200,200,200)),
            NavButton(option_button_rect,'Options',button_font,'white','black',GameState.OPTIONS,border_radius=3,alt_color=(200,200,200,200)),
        ]
        
    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.update(event,self.game)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill('aqua')
        # Render main menu elements here
        for button in self.buttons:
            button.draw(screen)
        screen_rect = screen.get_rect()
        Text('Ghost Survival',30).render(screen,center=screen_rect.center)
