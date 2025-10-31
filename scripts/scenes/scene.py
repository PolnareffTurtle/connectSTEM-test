import pygame

# Abstract class for all the screens in our game. 
class Scene:

    running = True
    
    def __init__(self, game):
        self.game = game

    def handle_events(self,events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass


class MainMenuScene(Scene):
    pass
