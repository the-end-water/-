import pygame
import json
import os
import sys
from config import *
from game.player import Player
from game.camera import Camera

class Map:
    def __init__(self, map_file_path , transition_zones ,video_zones=None):
        '''
        --1-- 首先从地图JSON文件加载地图信息
        '''
        self.map_data = None

        self.map_width = None

        self.map_height = None

        self.map_surface = None

        self.image = None

        self.image_path =  None

        self.collision_objects = []

        self.transition_zones = transition_zones

        self.video_zones = video_zones

        self.load_map(map_file_path)

        self.render_map()
        
        self.__get_obstacles()


    def load_map(self, map_file, if_show_obstacle = False):
        # 读取地图JSON文件
        with open(map_file, 'r', encoding='utf-8') as f:
            self.map_data = json.load(f)
        
        # 获取地图尺寸
        self.map_width = self.map_data["width"] * TILE_SIZE
        self.map_height = self.map_data["height"] * TILE_SIZE
        
        # 加载图块集
        self.tilesets = []
        for tileset in self.map_data["tilesets"]:
            if "image" in tileset:
                image_path = tileset["image"]

                # 简化路径处理 - 在实际项目中需要根据实际情况调整
                try:
                    # 尝试加载图片
                    image = pygame.image.load(os.path.join("assets", image_path.replace("../", "")))
                    
                    self.image_path = os.path.join("assets", image_path.replace("../", ""))
                    self.image = image 
                    
                    self.tilesets.append({
                        "firstgid": tileset["firstgid"],
                        "image": image,
                        "tilecount": tileset.get("tilecount", 0),
                        "columns": tileset.get("columns", 0)
                    })
                except:
                    print(f"无法加载图块集图片: {image_path}")
        
        # 创建地图表面
        self.map_surface = pygame.Surface((self.map_width, self.map_height))
        
        
    def render_map(self):
        # 渲染地图到表面
        self.map_surface.fill(BLACK)
        
        # 渲染每个图层
        for layer in self.map_data["layers"]:
            if layer["type"] == "tilelayer" and layer.get("visible", True):
                self.render_tile_layer(layer)
            elif layer["type"] == "imagelayer" and layer.get("visible", True):
                self.render_image_layer(layer) 

        # 渲染传送点
        for zone in self.transition_zones:
            pygame.draw.rect(self.map_surface, SAND_YELLOW, zone,border_radius=10)

        # 渲染视频播放点
        for zone in self.video_zones:
            pygame.draw.rect(self.map_surface, BROWN, zone,border_radius=10)
            

    def render_tile_layer(self, layer):
        data = layer["data"]
        width = layer["width"]
        height = layer["height"]
        
        for y in range(height):
            for x in range(width):
                tile_id = data[y * width + x]
                
                if tile_id == 0:  # 0表示空图块
                    continue

                # 找到对应的图块集
                for tileset in reversed(self.tilesets):
                    '''
                    testing 
                    '''
                    if tile_id >= 1:
                    # if tile_id >= tileset["firstgid"]:
                        # 计算图块在图块集中的位置
                    
                        local_id = (tile_id - tileset["firstgid"]) if (tile_id >= tileset["firstgid"] ) else  (tile_id-1)  # tileset["firstgid"] = 1025
                        tileset_cols = tileset["columns"] # tileset["columns"] = 32
                        
                        if tileset_cols > 0:
                            tx = (local_id % tileset_cols) * TILE_SIZE
                            ty = (local_id // tileset_cols) * TILE_SIZE
                            
                            # 绘制图块
                            self.map_surface.blit(
                                tileset["image"], 
                                (x * TILE_SIZE, y * TILE_SIZE),
                                (tx, ty, TILE_SIZE, TILE_SIZE)
                            )
                         
                        break

    def render_image_layer(self, layer): # 
        # print(os.path.join("assets", layer["image"].replace("../", "")))
        image_layer_img = pygame.image.load(os.path.join("assets", layer["image"].replace("../", "")))
        
        self.map_surface.blit(
            image_layer_img,
            (0,0)
            # (self.image_layer["x"] - camera_x, self.image_layer["y"] - camera_y)
        )

    def __get_obstacles(self):
        # 从对象层提取碰撞矩形
        for layer in self.map_data["layers"]:
            if layer.get("type") == "objectgroup" and layer.get("name") == "collision":
                for obj in layer["objects"]:
                    # 创建碰撞矩形
                    collision_rect = pygame.Rect(
                        obj["x"], 
                        obj["y"], 
                        obj["width"], 
                        obj["height"]
                    )
                    self.collision_objects.append(collision_rect)

    def draw(self,screen, camera_x, camera_y,SCREEN_WIDTH, SCREEN_HEIGHT):

        screen.blit(self.map_surface,(0,0),(camera_x, camera_y,SCREEN_WIDTH, SCREEN_HEIGHT))

        
    # def handle_events(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.running = False
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 self.running = False
        
    #     # 每当接受一次事件，更新玩家状态一次(或者更新所有精灵类一次)
    #     self.player.update(self.collision_objects)

    # def draw(self):  
    #     # 绘制地图
    #     self.screen.blit(self.map_surface, (0, 0), 
    #                     (self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT))
    #     # 绘制玩家
    #     # self.group.draw(self.screen)
    #     for sprite in self.group:
    #         self.screen.blit(sprite.image, (sprite.rect.x - self.camera.x, sprite.rect.y - self.camera.y))

    #     # self.player.draw(self.screen,self.camera_x, self.camera_y)

    #     #绘制碰撞矩形（调试用）
    #     for obj in self.collision_objects:
    #         pygame.draw.rect(self.screen, RED, 
    #                        (obj.x - self.camera.x, obj.y - self.camera.y, 
    #                         obj.width, obj.height), 1)
        
    #     pygame.display.flip()


