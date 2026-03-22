import pygame
import json
import math
import random

NEIGHBOR_OFFSETS = [
    (-1,-1), (0,-1), (1,-1),
    (-1,0),  (0,0),  (1,0),
    (-1,1),  (0,1),  (1,1),
]

tile_meta = dict()
with open('assets/tiled/spritesheet.json') as f:
    rawjson = f.read()
    jsondata = json.loads(rawjson)
    for tile in jsondata.get('tiles', []):
        tile_meta[tile['id']] = tile

FLOOR_TILE = 0
WALL_TILE  = 1

class Tile:
    def __init__(self, tile_index, pos, rotation=0):
        self.index = tile_index
        self.pos = pos
        meta = tile_meta.get(tile_index, {})
        self.type = meta.get('type', None)
        props = {}
        for p in meta.get('properties', []):
            props[p.get('name')] = p.get('value')
        self.properties = props
        self.rotation = rotation

class Tilemap:
    def __init__(self, scene, map=None, tile_size=16, procedural=False,
                 map_width=80, map_height=60, seed=None):
        self.scene = scene
        self.map = map
        self.tile_size = tile_size
        self.tilemap = dict()
        self.spawns = []
        self.room_positions: set[tuple[int, int]] = set()

        if procedural:
            self._generate_rooms(map_width, map_height, seed)
        else:
            self.open_json(map)

    def open_json(self, map):
        with open('assets/tiled/maps/' + str(map) + '.json') as f:
            rawjson = f.read()
            jsondata = json.loads(rawjson)

        self.width  = jsondata['width']
        self.height = jsondata['height']

        for j, val in enumerate(jsondata['layers'][0]['data']):
            x = j % jsondata['width']
            y = j // jsondata['width']
            if val != 0:
                tile = Tile(val - 1, (x, y))
                if tile.type == 'spawn' and tile.properties.get('entity'):
                    px = tile.pos[0] * self.tile_size + (self.tile_size // 2)
                    py = tile.pos[1] * self.tile_size + (self.tile_size // 2)
                    self.spawns.append({'pos': (px, py), 'entity': tile.properties.get('entity'), 'subclass': tile.properties.get('subclass', None)})
                self.tilemap[(x, y)] = tile

    def _generate_rooms(self, map_width, map_height, seed, min_room=6, max_room=14):
        rng = random.Random(seed)
        self.width  = map_width
        self.height = map_height
        raw: dict[tuple[int, int], int] = {}

        def split(x, y, w, h, depth=0):
            min_split = min_room + 2
            can_h = h >= min_split * 2
            can_v = w >= min_split * 2
            if not can_h and not can_v or depth > 6:
                return [(x, y, w, h)]
            if can_h and can_v:
                horiz = rng.random() < 0.5
            else:
                horiz = can_h
            if horiz:
                cut = rng.randint(y + min_split, y + h - min_split)
                return split(x, y, w, cut - y, depth+1) + split(x, cut, w, y + h - cut, depth+1)
            else:
                cut = rng.randint(x + min_split, x + w - min_split)
                return split(x, y, cut - x, h, depth+1) + split(cut, y, x + w - cut, h, depth+1)

        partitions = split(0, 0, map_width, map_height)

        rooms = []
        for (px, py, pw, ph) in partitions:
            rw = rng.randint(min_room, min(max_room, pw - 2))
            rh = rng.randint(min_room, min(max_room, ph - 2))
            rx = rng.randint(px + 1, px + pw - rw - 1)
            ry = rng.randint(py + 1, py + ph - rh - 1)
            rooms.append((rx, ry, rw, rh))
            for tx in range(rx, rx + rw):
                for ty in range(ry, ry + rh):
                    raw[(tx, ty)] = FLOOR_TILE

        for i in range(len(rooms) - 1):
            ax = rooms[i][0] + rooms[i][2] // 2
            ay = rooms[i][1] + rooms[i][3] // 2
            bx = rooms[i+1][0] + rooms[i+1][2] // 2
            by = rooms[i+1][1] + rooms[i+1][3] // 2
            if rng.random() < 0.5:
                for x in range(min(ax, bx), max(ax, bx) + 1): raw[(x, ay)] = FLOOR_TILE
                for y in range(min(ay, by), max(ay, by) + 1): raw[(bx, y)] = FLOOR_TILE
            else:
                for y in range(min(ay, by), max(ay, by) + 1): raw[(ax, y)] = FLOOR_TILE
                for x in range(min(ax, bx), max(ax, bx) + 1): raw[(x, by)] = FLOOR_TILE

        offsets = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        for (fx, fy) in list(raw.keys()):
            for dx, dy in offsets:
                nb = (fx+dx, fy+dy)
                if 0 <= nb[0] < map_width and 0 <= nb[1] < map_height and nb not in raw:
                    raw[nb] = WALL_TILE

        for (tx, ty), idx in raw.items():
            self.tilemap[(tx, ty)] = Tile(idx, (tx, ty))

        self.room_positions = {
            (r[0] * self.tile_size + r[2] * self.tile_size // 2,
             r[1] * self.tile_size + r[3] * self.tile_size // 2)
            for r in rooms
        }

        if self.room_positions:
            self.spawns.append({'pos': next(iter(self.room_positions)), 'entity': 'player', 'subclass': None})

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (tile_loc[0]+offset[0], tile_loc[1]+offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.type == 'physics':
                rects.append(pygame.rect.Rect(tile.pos[0]*self.tile_size, tile.pos[1]*self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset):
        for x in range(math.floor(offset[0]/self.tile_size), math.ceil((offset[0]+surf.get_width())/self.tile_size)):
            for y in range(math.floor(offset[1]/self.tile_size), math.ceil((offset[1]+surf.get_height())/self.tile_size)):
                if (x, y) in self.tilemap:
                    tile = self.tilemap[(x, y)]
                    surf.blit(self.scene.game.assets['tiles'][tile.index],
                              (tile.pos[0]*self.tile_size - offset[0], tile.pos[1]*self.tile_size - offset[1]))