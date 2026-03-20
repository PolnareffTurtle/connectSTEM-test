import pygame
from scripts.scenes.scene import Scene
from scripts.button import NavButton, Button
from scripts.enums import GameState
from scripts.utils import Text
from scripts.music import Music


SLIDER_WIDTH = 80
SLIDER_HEIGHT = 6
SLIDER_KNOB_RADIUS = 6


class OptionsMenuScene(Scene):
    gamestate = GameState.OPTIONS
    def __init__(self, game):
        super().__init__(game)
        self.muted = Music.muted
        button_font = pygame.font.Font('assets/fonts/pixel.ttf', 10)
        mute_button_rect = pygame.Rect(0, 0, 90, 20)
        change_res_button_rect = pygame.Rect(0, 0, 120, 20)
        back_button_rect = pygame.Rect(0, 0, 50, 20)

        mute_button_rect.center = game.display.get_width() // 2, 70
        change_res_button_rect.center = game.display.get_width() // 2, 100
        back_button_rect.center = game.display.get_width() // 2, game.display.get_height() // 2 + 65
        self.button_color = (255, 255, 255, 200)
        self.button_hover_color = (200, 200, 200, 200)

        self.slider_label_y = 10
        self.slider_rect = pygame.Rect(0, 0, SLIDER_WIDTH, SLIDER_HEIGHT)
        self.slider_rect.midleft = (game.display.get_width() // 2 + 60, 40)
        self.slider_dragging = False
        self.volume = pygame.mixer.music.get_volume() if pygame.mixer.get_init() else 1.0

        # Resolution
        self.show_resolution_menu = False

        self.resolution_options = [
            (1280, 720),
            (1600, 900),
            (1920, 1080),
            (800, 450),
        ]


        self.resolution_buttons = []

        center_x = game.display.get_width() // 2
        start_y = 110
        row_spacing = 24
        col_offset = 50

        for i, (w, h) in enumerate(self.resolution_options):
            col = i % 2
            row = i // 2
            x = center_x - col_offset if col == 0 else center_x + col_offset
            y = start_y + row * row_spacing
            r = pygame.Rect(0, 0, 80, 14)
            r.center = (x, y)

            self.resolution_buttons.append(
                Button(r, f"{w}x{h}", button_font, self.button_color, (0, 0, 0), border_radius=3)
            )

        self.buttons = [
            Button(mute_button_rect, 'Unmute Music' if self.muted else 'Mute Music', button_font, self.button_color, (0, 0, 0), border_radius=3),
            Button(change_res_button_rect, 'Change Resolution', button_font, self.button_color, (0, 0, 0), border_radius=3),
            NavButton(back_button_rect, 'Back', button_font, 'white', 'black', GameState.MAIN_MENU, border_radius=3, alt_color=(200, 200, 200, 200))
        ]

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            scale_x, scale_y = self.game.scale
            mouse_pos = (mouse_pos[0] / scale_x, mouse_pos[1] / scale_y)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_button = self.buttons[0]
                if mute_button.rect.collidepoint(mouse_pos):
                    Music.toggle_mute()
                    self.muted = Music.muted

                    Music.update(pygame.event.Event(pygame.NOEVENT), self.game.gamestate)

                    mute_button.text = 'Unmute Music' if self.muted else 'Mute Music'
                    if hasattr(mute_button, 'update_text'):
                        mute_button.update_text()

                change_res_button = self.buttons[1]
                if change_res_button.rect.collidepoint(mouse_pos):
                    self.show_resolution_menu = not self.show_resolution_menu

                knob_x = self.slider_rect.x + int(self.volume * self.slider_rect.width)
                knob_rect = pygame.Rect(0, 0, SLIDER_KNOB_RADIUS * 2, SLIDER_KNOB_RADIUS * 2)
                knob_rect.center = (knob_x, self.slider_rect.centery)
                hit_rect = self.slider_rect.inflate(12, 12)
                if hit_rect.collidepoint(mouse_pos) or knob_rect.collidepoint(mouse_pos):
                    self.slider_dragging = True
                    relative_x = max(0, min(mouse_pos[0] - self.slider_rect.x, self.slider_rect.width))
                    self.volume = relative_x / self.slider_rect.width
                    pygame.mixer.music.set_volume(self.volume)

                if self.show_resolution_menu:
                    for res_btn, (w, h) in zip(self.resolution_buttons, self.resolution_options):
                        if res_btn.rect.collidepoint(mouse_pos):
                            self.game.screen = pygame.display.set_mode((w, h))
                            self.show_resolution_menu = False
                            break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.slider_dragging = False

            elif event.type == pygame.MOUSEMOTION and self.slider_dragging:
                relative_x = max(0, min(mouse_pos[0] - self.slider_rect.x, self.slider_rect.width))
                self.volume = relative_x / self.slider_rect.width
                pygame.mixer.music.set_volume(self.volume)

            for button in self.buttons:
                button.update(event, self.game)

            if self.show_resolution_menu:
                for button in self.resolution_buttons:
                    button.update(event, self.game)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill('aqua')

        mouse_pos = pygame.mouse.get_pos()
        scale_x, scale_y = self.game.scale
        mouse_pos = (mouse_pos[0] / scale_x, mouse_pos[1] / scale_y)

        for i, button in enumerate(self.buttons):
            if i < 2:
                button.bg_color = self.button_hover_color if button.rect.collidepoint(mouse_pos) else self.button_color
            button.draw(screen)

        if self.show_resolution_menu:
            for button in self.resolution_buttons:
                button.bg_color = self.button_hover_color if button.rect.collidepoint(mouse_pos) else self.button_color
                button.draw(screen)

        Text('Options', 24).render(screen, topleft=(10, 4))
        Text('Volume', 18).render(screen, center=(self.slider_rect.x - 60, self.slider_rect.centery))

        pygame.draw.rect(screen, (180, 180, 180), self.slider_rect, border_radius=3)
        filled_rect = pygame.Rect(self.slider_rect.x, self.slider_rect.y, int(self.slider_rect.width * self.volume), self.slider_rect.height)
        pygame.draw.rect(screen, (255, 255, 255), filled_rect, border_radius=3)

        knob_x = self.slider_rect.x + int(self.volume * self.slider_rect.width)
        knob_x = max(self.slider_rect.left, min(knob_x, self.slider_rect.right))
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.slider_rect.centery), SLIDER_KNOB_RADIUS)
        pygame.draw.circle(screen, (0, 0, 0), (knob_x, self.slider_rect.centery), SLIDER_KNOB_RADIUS, 1)