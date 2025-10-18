from enum import Enum

class GameState(Enum):
    GAME_MENU = 0
    GAME_RUNNING = 1

class WeaponType(Enum):
    CIRCLE = 'circle',
    PROJECTILE = 'projectile',
    LUNGE = 'lunge',
    NONE = 'none'
