import pygame
import json
import os
from typing import Dict, List, Tuple, Optional
from config import TILE_SIZE, SPRITES_PATH
from graphics.sprite_loader import SpriteLoader

# 图块 类
class Tile:
    """单个图块类"""
    """
        初始化单个图块
        
        参数:
            tile_id: 图块序号(int)
            image: 图块的加载图片(pygame.Surface)
            properties: 图块属性, 字典类型, 推荐包含"是否可碰撞","是否动态",
                {
                'collidable':  ,
                'animated': 
                }

    """
    def __init__(self, tile_id: int, image: pygame.Surface, properties: dict = None):

        self.tile_id = tile_id
        self.image = image
        self.properties = properties or {}

        self.collidable = properties.get('collidable', False) if properties else False
        self.animated = properties.get('animated', False) if properties else False
        
    def render(self, surface: pygame.Surface, x: int, y: int):
        """在指定位置渲染图块"""
        surface.blit(self.image, (x, y))

class TileLayer:
    """图块层类，包含一层图块数据"""
    """
        初始化图块层(图块矩阵)
        
        参数:
            name: 图块名字
            width: 图块层宽度(int)
            height: 图块层高度(int)
            data: 列表，内容是图块序号
           
    """
    def __init__(self, name: str, width: int, height: int, data: List[int] = None):
        self.name = name
        self.width = width
        self.height = height
        self.data = data or [0] * (width * height)  # 0表示空图块

        self.visible = True
        self.opacity = 1.0
        
    def get_tile(self, x: int, y: int) -> int:
        """获取指定位置的图块ID"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y * self.width + x]
        return 0
    
    def set_tile(self, x: int, y: int, tile_id: int):
        """设置指定位置的图块ID"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.data[y * self.width + x] = tile_id
    
    def fill(self, tile_id: int):
        """用指定图块ID填充整个层"""
        self.data = [tile_id] * (self.width * self.height)


class Tileset:
    """图块集管理类"""
    """
        初始化图块集
        
        参数:
            name: 图块名字
            width: 图块层宽度(int)
            height: 图块层高度(int)
            data: 列表，内容是图块序号
           
    """
    def __init__(self):
        self.sprite_loader = SpriteLoader()
        self.tilesets: Dict[str, Dict] = {}  # 图块集定义
        self.tiles: Dict[int, Tile] = {}     # 全局图块索引
        self.next_tile_id = 1
        
    def load_tileset_definition(self, name: str, filename: str) -> bool:
        """加载图块集定义文件（JSON格式）"""
        """
        参数:
            name: 定义图块名字
            filename: 图块所在文件名字
           
        """
        filepath = os.path.join(SPRITES_PATH, "tilesets", filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # 加载字典格式的图块数据
                tileset_data = json.load(f)
            
            # 解析图块集数据
            image_file = tileset_data.get("image", "")
            tile_width = tileset_data.get("tilewidth", TILE_SIZE)
            tile_height = tileset_data.get("tileheight", TILE_SIZE)
            first_gid = tileset_data.get("firstgid", self.next_tile_id)
            
            # 加载图块图像
            tiles = self.sprite_loader.load_spritesheet(
                f"tilesets/{image_file}", tile_width, tile_height
            )
            
            # 处理图块属性
            tile_properties = tileset_data.get("tileproperties", {})
            tileset_properties = tileset_data.get("properties", {})
            
            # 注册图块
            for i, tile_image in enumerate(tiles):
                tile_id = first_gid + i
                properties = {}
                
                # 合并图块特定属性和图块集通用属性
                if str(i) in tile_properties:
                    properties.update(tile_properties[str(i)])
                properties.update(tileset_properties)
                
                tile = Tile(tile_id, tile_image, properties)
                self.tiles[tile_id] = tile
            
            # 存储图块集信息
            self.tilesets[name] = {
                "first_gid": first_gid,
                "tile_count": len(tiles),
                "tile_width": tile_width,
                "tile_height": tile_height,
                "image": image_file
            }
            
            self.next_tile_id = first_gid + len(tiles)
            print(f"加载图块集 '{name}'，包含 {len(tiles)} 个图块")
            return True
            
        except Exception as e:
            print(f"加载图块集失败 {filename}: {e}")
            return False
    
    def load_from_tiled_json(self, level_data: dict) -> Tuple[List[TileLayer], List[List[bool]]]:
        """从Tiled编辑器导出的JSON加载关卡数据"""
        """
        参数:
            level_data: 从Tiled编辑器导出的JSON加载关卡数据
           
        """
        layers = []
        collision_layer = []
        
        # 首先加载所有图块集，获得"名字，路径"，并加载
        for tileset_data in level_data.get("tilesets", []):
            # 获得图块集名字
            name = tileset_data.get("name", "unknown")

            # 获得图块集的图片路径
            image_file = os.path.basename(tileset_data.get("image", ""))

            # 使用图片路径创建图块集
            self.load_tileset_definition(name, image_file)
        
        # 创建碰撞层（初始化为全False）
        map_width = level_data["width"]
        map_height = level_data["height"]
        collision_layer = [[False] * map_width for _ in range(map_height)]
        
        # 处理图层
        for layer_data in level_data.get("layers", []):
            layer_type = layer_data.get("type", "tilelayer")
            
            if layer_type == "tilelayer":
                layer = TileLayer(
                    layer_data["name"],
                    layer_data["width"],
                    layer_data["height"],
                    layer_data["data"]
                )
                layers.append(layer)
                
                # 如果是碰撞层，更新碰撞数据
                if layer_data.get("properties", {}).get("collision", False):
                    self._update_collision_layer(layer, collision_layer)
            
            elif layer_type == "objectgroup" and layer_data["name"] == "collision":
                # 处理对象层中的碰撞对象
                self._process_collision_objects(layer_data, collision_layer)
        
        return layers, collision_layer
    
    def _update_collision_layer(self, layer: TileLayer, collision_layer: List[List[bool]]):
        """根据图块层更新碰撞层"""
        for y in range(layer.height):
            for x in range(layer.width):
                tile_id = layer.get_tile(x, y)
                if tile_id > 0 and tile_id in self.tiles:
                    if self.tiles[tile_id].collidable:
                        collision_layer[y][x] = True
    
    def _process_collision_objects(self, object_layer: dict, collision_layer: List[List[bool]]):
        """处理对象层中的碰撞对象"""
        for obj in object_layer.get("objects", []):
            x = int(obj["x"] // TILE_SIZE)
            y = int(obj["y"] // TILE_SIZE)
            width = int(obj.get("width", TILE_SIZE) // TILE_SIZE)
            height = int(obj.get("height", TILE_SIZE) // TILE_SIZE)
            
            # 标记碰撞区域
            for dy in range(height):
                for dx in range(width):
                    if 0 <= y + dy < len(collision_layer) and 0 <= x + dx < len(collision_layer[0]):
                        collision_layer[y + dy][x + dx] = True
    
    def get_tile(self, tile_id: int) -> Optional[Tile]:
        """根据ID获取图块"""
        return self.tiles.get(tile_id)
    
    def is_tile_collidable(self, tile_id: int) -> bool:
        """检查图块是否可碰撞"""
        tile = self.get_tile(tile_id)
        return tile.collidable if tile else False
    
    def render_layer(self, surface: pygame.Surface, layer: TileLayer, offset_x: int = 0, offset_y: int = 0):
        """渲染图块层"""
        if not layer.visible:
            return
            
        for y in range(layer.height):
            for x in range(layer.width):
                tile_id = layer.get_tile(x, y)
                if tile_id > 0 and tile_id in self.tiles:
                    screen_x = x * TILE_SIZE - offset_x
                    screen_y = y * TILE_SIZE - offset_y
                    
                    # 只渲染在屏幕范围内的图块
                    if (-TILE_SIZE <= screen_x < surface.get_width() and 
                        -TILE_SIZE <= screen_y < surface.get_height()):
                        self.tiles[tile_id].render(surface, screen_x, screen_y)
    
    def render_tile(self, surface: pygame.Surface, tile_id: int, x: int, y: int):
        """在指定位置渲染单个图块"""
        if tile_id in self.tiles:
            self.tiles[tile_id].render(surface, x, y)
    
    def create_collision_map_from_layers(self, layers: List[TileLayer]) -> List[List[bool]]:
        """从图层数据创建碰撞地图"""
        if not layers:
            return []
            
        width = layers[0].width
        height = layers[0].height
        collision_map = [[False] * width for _ in range(height)]
        
        for layer in layers:
            for y in range(height):
                for x in range(width):
                    tile_id = layer.get_tile(x, y)
                    if self.is_tile_collidable(tile_id):
                        collision_map[y][x] = True
        
        return collision_map
    
    def get_tileset_info(self, name: str) -> Optional[Dict]:
        """获取图块集信息"""
        return self.tilesets.get(name)
    
    def get_all_tilesets(self) -> Dict[str, Dict]:
        """获取所有图块集"""
        return self.tilesets
    
    def clear(self):
        """清空所有图块数据"""
        self.tilesets.clear()
        self.tiles.clear()
        self.next_tile_id = 1

# 单例模式，方便全局访问
_tileset_instance = None

def get_tileset() -> Tileset:
    """获取图块集单例"""
    global _tileset_instance
    if _tileset_instance is None:
        _tileset_instance = Tileset()
    return _tileset_instance


