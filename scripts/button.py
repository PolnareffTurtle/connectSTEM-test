import pygame
from scripts.enums import GameState

class Button:
    def __init__(self, rect, text, font, bg_color, text_color, border_radius=0):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.border_radius = border_radius
        self.bg_color = bg_color
        self.text_color = text_color
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)
        self.hovered = False

    def draw(self, screen):
        temp_surf = pygame.Surface(self.rect.size,pygame.SRCALPHA)
        temp_rect = self.rect.copy()
        temp_rect.topleft = 0,0
        temp_text_rect = self.text_rect.copy()
        temp_text_rect.topleft = self.text_rect.x - self.rect.x, self.text_rect.y - self.rect.y
        pygame.draw.rect(temp_surf, self.bg_color, temp_rect, border_radius=self.border_radius)
        temp_surf.blit(self.rendered_text, temp_text_rect)
        screen.blit(temp_surf,self.rect)

    def update(self,event,game):
        if self.is_clicked(event, game):
            self.on_click(game)
        if self.is_hovered(event, game):
            self.hovered = True
            self.on_hover(game)
        else:
            self.hovered = False

    def is_clicked(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0]//game.scale[0],event.pos[1]//game.scale[1])
            if self.rect.collidepoint(pos):
                return True
        return False
    
    def is_hovered(self, event, game):
        pos = pygame.mouse.get_pos()
        pos = (pos[0]//game.scale[0],pos[1]//game.scale[1])
        if self.rect.collidepoint(pos):
            return True
        return False
        
    def on_click(self,game):
        pass

    def on_hover(self,game):
        pass

class NavButton(Button):
    def __init__(self, rect, text, font, bg_color, text_color, target_scene: GameState, border_radius=0, alt_color = 'white'):
        super().__init__(rect, text, font, bg_color, text_color, border_radius)
        self.target_scene = target_scene
        self.alt_color = alt_color
        self.first_color = bg_color

    def on_click(self, game):
        game.change_scene(self.target_scene)

    def draw(self, screen):
        if self.hovered:
            self.bg_color = self.alt_color
        else:
            self.bg_color = self.first_color
        super().draw(screen)

# this is primarily for the pause button
class StopSceneButton(NavButton):

    def on_click(self, game):
        game.scene.running = False
