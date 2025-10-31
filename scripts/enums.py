from enum import Enum

class GameState(Enum):
    GAME_MENU = 0
    GAMEPLAY = 1

class WeaponType(Enum):
    CIRCLE = 'circle',
    PROJECTILE = 'projectile',
    LUNGE = 'lunge',
    ROTATE = 'rotate',
    NONE = 'none'

class ItemType(Enum):
    NONE = 'none',
    COIN = 'coin'
