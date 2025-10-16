import pygame
import json
import math

NEIGHBOR_OFFSETS = [
    (-1,-1), (0,-1), (1,-1),
    (-1,0),  (0,0),  (1,0),
    (-1,1),  (0,1),  (1,1),
]

# read each tile type in spritesheet.json
tile_types = dict()
with open('assets/tiled/spritesheet.json') as f:
    rawjson = f.read()
    jsondata = json.loads(rawjson)
    for tile in jsondata['tiles']:
        tile_types[tile['id']] = tile['type']

class Tile:
    def __init__(self, tile_index, pos, rotation=0):
        self.index = tile_index
        self.pos = pos
        self.type = tile_types.get(tile_index,None)
        self.rotation = rotation

class Tilemap:
    def __init__(self,game,level,tile_size=16):
        self.game=game
        self.level=level
        self.tile_size = tile_size
        self.tilemap = dict()
        self.open_json(level)

    def open_json(self,map):
        with open('assets/tiled/maps/'+str(map)+'.json') as f:
            rawjson = f.read()
            jsondata = json.loads(rawjson)

        self.width = jsondata['width']
        self.height = jsondata['height']
        
        # set player x,y to whats defined in the tiled map properties
        self.game.player.pos[0] = jsondata['properties'][0]['value'] * self.tile_size
        self.game.player.pos[1] = jsondata['properties'][1]['value'] * self.tile_size

        for j,val in enumerate(jsondata['layers'][0]['data']):
            x = j % jsondata['width']
            y = j // jsondata['width']

            if val != 0:
                self.tilemap[(x, y)] = Tile(val - 1, (x, y))

    def tiles_around(self,pos):
        tiles=[]
        tile_loc = (int(pos[0] // self.tile_size),int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (tile_loc[0]+offset[0], tile_loc[1]+offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self,pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.type == 'physics':
                rects.append(pygame.rect.Rect(tile.pos[0]*self.tile_size,tile.pos[1]*self.tile_size,self.tile_size,self.tile_size))
        return rects

    def render(self,surf,offset):
        for x in range(math.floor(offset[0] / self.tile_size),math.ceil((offset[0] + surf.get_width()) / self.tile_size)):
            for y in range(math.floor(offset[1] / self.tile_size),math.ceil((offset[1] + surf.get_height()) / self.tile_size)):
                if (x, y) in self.tilemap:
                    tile = self.tilemap[(x, y)]
                    surf.blit(
                        self.game.assets['tiles'][tile.index],
                        (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))
