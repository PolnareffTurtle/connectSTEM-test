from scripts.powerup import PowerUp
from scripts.scenes.scene import Scene
from scripts.button import StopSceneButton,NavButton
from scripts.enums import GameState
from scripts.utils import Text
import pygame

class PowerUpSelectionScreen(Scene):
    def __init__(self,game):
        super().__init__(game)
        self.display = pygame.Surface((game.display.get_width()*0.8,game.display.get_height()*0.8),pygame.SRCALPHA)
        overlay = pygame.Surface(game.display.get_size(),pygame.SRCALPHA)
        overlay.fill((120,120,120,200))
        game.display.blit(overlay,(0,0))
        self.display_rect = pygame.rect.Rect((0,0),self.display.get_size())
        self.display_rect.center = game.display.get_width() //2 , game.display.get_height() //2
        self.main_text_surf = Text('Choose a powerup!', 10)
        self.main_text_pos = (game.display.get_width()//2,game.display.get_height()//4)
        self.powerup_options = ["Speed boost",
                           "Shield",
                           "Coin multiplier"]
        pause_button_rect = pygame.rect.Rect(0,0,20,20)
        pause_button_rect.topright = (self.display_rect.right-10,self.display_rect.top+10)
        button_font = pygame.font.Font('assets/fonts/pixel.ttf',10)
        self.buttons = [
            StopSceneButton(pause_button_rect,'X',button_font,(255,255,255,200),(255,0,0),GameState.GAMEPLAY,border_radius=3,alt_color=(200,200,200,200))
        ]
        self.selection = 0

    def handle_events(self,events):
        for event in events:
            for button in self.buttons:
                button.update(event,self.game)

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN]:
                    self.selection = (self.selection + 1) % len(self.powerup_options)
                if event.key in [pygame.K_UP]:
                    self.selection = (self.selection - 1) % len(self.powerup_options)

                # work in progress since this is pretty messy / not very modular
                if event.key == pygame.K_RETURN:
                    if self.selection == 0:
                        self.game.scene_stack[-1].powerups.append(PowerUp("speed", 5))
                    if self.selection == 1:
                        self.game.scene_stack[-1].powerups.append(PowerUp("shield", 8))
                    if self.selection == 2:
                        self.game.scene_stack[-1].powerups.append(PowerUp("coin_multiplier", 10))
                    self.game.scene_stack[-1].powerups[-1].apply(self.game.scene_stack[-1].player, self.game.scene_stack[-1].wallet)
                    self.running = False

    def update(self,dt):
        pass

    def render(self,screen):
        self.display.fill((220,220,220,100))
        screen.blit(self.display,(
            (screen.get_width()-self.display.get_width())//2,
            (screen.get_height()-self.display.get_height())//2))
        for button in self.buttons:
            button.draw(screen)
        for i in range(len(self.powerup_options)):
            if i == self.selection:
                Text(self.powerup_options[i],10,color="black").render(screen, center=(self.game.display.get_width()//2,self.game.display.get_height()//2 + 10 * i))
            else:
                Text(self.powerup_options[i],10,color="grey").render(screen, center=(self.game.display.get_width()//2,self.game.display.get_height()//2 + 10 * i))
        self.main_text_surf.render(screen,center=self.main_text_pos)