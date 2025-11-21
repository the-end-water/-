
import pygame
import os
from config import SPRITES_PATH

class SpriteLoader:
    def __init__(self):
        self.sprites = {}
        self.tilesets = {}
        
    def load_spritesheet(self, filename, sprite_width, sprite_height):
        """加载精灵表并分割成单个精灵"""
        filepath = os.path.join(SPRITES_PATH, filename)
        if not os.path.exists(filepath):
            print(f"警告: 文件 {filepath} 不存在")
            return []
            
        sheet = pygame.image.load(filepath).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        
        sprites = []
        for y in range(0, sheet_height, sprite_height):
            for x in range(0, sheet_width, sprite_width):
                rect = pygame.Rect(x, y, sprite_width, sprite_height)
                sprite = sheet.subsurface(rect)
                sprites.append(sprite)
                
        return sprites
    
    def load_tileset(self, name, filename, tile_size):
        """加载图块集"""
        tiles = self.load_spritesheet(f"tilesets/{filename}", tile_size, tile_size)
        self.tilesets[name] = tiles
        return tiles
    
    
    def get_tile(self, tileset_name, tile_id):
        """获取指定图块"""
        if tileset_name in self.tilesets and tile_id < len(self.tilesets[tileset_name]):
            return self.tilesets[tileset_name][tile_id]
        return None