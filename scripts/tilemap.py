import pygame
import json
import math

NEIGHBOR_OFFSETS = [
    (-1,-1), (0,-1), (1,-1),
    (-1,0),  (0,0),  (1,0),
    (-1,1),  (0,1),  (1,1),
]

# read each tile type in spritesheet.json
tile_meta = dict()
with open('assets/tiled/spritesheet.json') as f:
    rawjson = f.read()
    jsondata = json.loads(rawjson)
    for tile in jsondata.get('tiles', []):
        # store the full metadata so we can access type and properties
        tile_meta[tile['id']] = tile

class Tile:
    def __init__(self, tile_index, pos, rotation=0):
        self.index = tile_index
        self.pos = pos
        meta = tile_meta.get(tile_index, {})
        self.type = meta.get('type', None)
        # convert properties list to a dict for easy lookup
        props = {}
        for p in meta.get('properties', []):
            props[p.get('name')] = p.get('value')
        self.properties = props
        self.rotation = rotation

class Tilemap:
    def __init__(self,scene,map,tile_size=16):
        self.scene=scene
        self.map=map
        self.tile_size = tile_size
        self.tilemap = dict()
        # discovered spawn points: list of {'pos':(px,py),'entity':str}
        self.spawns = []
        self.open_json(map)

    def open_json(self,map):
        with open('assets/tiled/maps/'+str(map)+'.json') as f:
            rawjson = f.read()
            jsondata = json.loads(rawjson)

        self.width = jsondata['width']
        self.height = jsondata['height']

        for j,val in enumerate(jsondata['layers'][0]['data']):
            x = j % jsondata['width']
            y = j // jsondata['width']

            if val != 0:
                tile = Tile(val - 1, (x, y))
                # collect spawn tiles (type == 'spawn' and an 'entity' property)
                if tile.type == 'spawn' and tile.properties.get('entity'):
                    px = tile.pos[0] * self.tile_size + (self.tile_size // 2)
                    py = tile.pos[1] * self.tile_size + (self.tile_size // 2)
                    self.spawns.append({'pos': (px, py), 'entity': tile.properties.get('entity'), 'subclass': tile.properties.get('subclass', None)})
                self.tilemap[(x, y)] = tile

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
                        self.scene.game.assets['tiles'][tile.index],
                        (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))
