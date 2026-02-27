from enum import Enum

class GameState(Enum):
    MAIN_MENU = 'main_menu'
    GAMEPLAY = 'gameplay'
    PAUSE = 'pause'
    DEATH = 'death'

class WeaponType(Enum):
    CIRCLE = 'circle',
    PROJECTILE = 'projectile',
    LUNGE = 'lunge',
    ROTATE = 'rotate',
    NONE = 'none'

class ItemType(Enum):
    NONE = 'none',
    COIN = 'coin'
