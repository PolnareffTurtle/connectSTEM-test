from scripts.scenes.scene import Scene
from scripts.button import StopSceneButton,NavButton
from scripts.enums import GameState
from scripts.utils import Text
import pygame

class PauseScene(Scene):
    def __init__(self,game):
        super().__init__(game)
        self.display = pygame.Surface((game.display.get_width()*0.8,game.display.get_height()*0.8),pygame.SRCALPHA)
        overlay = pygame.Surface(game.display.get_size(),pygame.SRCALPHA)
        overlay.fill((120,120,120,200))
        game.display.blit(overlay,(0,0))
        self.display_rect = pygame.rect.Rect((0,0),self.display.get_size())
        self.display_rect.center = game.display.get_width() //2 , game.display.get_height() //2 
        pause_button_rect = pygame.rect.Rect(0,0,20,20)
        pause_button_rect.topright = (self.display_rect.right-10,self.display_rect.top+10)
        home_button_rect = pygame.rect.Rect(0,0,50,20)
        home_button_rect.bottomleft = (self.display_rect.left+2,self.display_rect.bottom-2)
        button_font = pygame.font.Font('assets/fonts/pixel.ttf',10)
        self.buttons = [
            StopSceneButton(pause_button_rect,'X',button_font,(255,255,255,200),(255,0,0),GameState.GAMEPLAY,border_radius=3,alt_color=(200,200,200,200)),
            NavButton(home_button_rect,'Quit',button_font,(255,255,255),(0,0,0),GameState.MAIN_MENU,border_radius=2,alt_color=(200,200,200))
        ]

    def handle_events(self,events):
        for event in events:
            for button in self.buttons:
                button.update(event,self.game)

    def update(self,dt):
        pass

    def render(self,screen):
        self.display.fill((220,220,220,100))
        screen.blit(self.display,(
            (screen.get_width()-self.display.get_width())//2,
            (screen.get_height()-self.display.get_height())//2))
        for button in self.buttons:
            button.draw(screen)
        Text('Game Paused',10).render(screen,topleft=(self.display_rect.x+10,self.display_rect.y+10))
        
        
        
