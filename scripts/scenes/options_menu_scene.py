import pygame
from scripts.scenes.scene import Scene
from scripts.button import NavButton, Button
from scripts.enums import GameState
from scripts.utils import Text
from scripts.music import Music


class OptionsMenuScene(Scene):
    gamestate = GameState.OPTIONS
    def __init__(self, game):
        super().__init__(game)
        self.muted = Music.muted
        button_font = pygame.font.Font('assets/fonts/pixel.ttf', 10)
        mute_button_rect = pygame.Rect(0, 0, 90, 20)
        change_res_button_rect = pygame.Rect(0, 0, 120, 20)
        back_button_rect = pygame.Rect(0, 0, 50, 20)

        mute_button_rect.center = game.display.get_width() // 2, 60
        change_res_button_rect.center = game.display.get_width() // 2, 85
        back_button_rect.center = game.display.get_width() // 2, game.display.get_height() // 2 + 65

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
                Button(r, f"{w}x{h}", button_font, (255, 255, 255, 200), (0, 0, 0), border_radius=3)
            )

        self.buttons = [
            Button(mute_button_rect, 'Unmute Music' if self.muted else 'Mute Music', button_font, (255, 255, 255, 200), (0, 0, 0), border_radius=3),
            Button(change_res_button_rect, 'Change Resolution', button_font, (255, 255, 255, 200), (0, 0, 0), border_radius=3),
            NavButton(back_button_rect, 'Back', button_font, 'white', 'black', GameState.MAIN_MENU, border_radius=3, alt_color=(200, 200, 200, 200))
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                scale_x, scale_y = self.game.scale
                mouse_pos = (mouse_pos[0] / scale_x, mouse_pos[1] / scale_y)

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

                if self.show_resolution_menu:
                    for res_btn, (w, h) in zip(self.resolution_buttons, self.resolution_options):
                        if res_btn.rect.collidepoint(mouse_pos):
                            self.game.screen = pygame.display.set_mode((w, h))
                            self.show_resolution_menu = False
                            break

            for button in self.buttons:
                button.update(event, self.game)

            if self.show_resolution_menu:
                for button in self.resolution_buttons:
                    button.update(event, self.game)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill('aqua')
        for button in self.buttons:
            button.draw(screen)

        if self.show_resolution_menu:
            for button in self.resolution_buttons:
                button.draw(screen)

        Text('Options', 24).render(screen, topleft=(10, 4))