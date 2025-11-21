import pygame
import json
import os
import sys
from config import *

class Camera:
    def __init__(self, map_width ,map_height ,x=0, y=0):
        self.x = x
        self.y = y
        self.map_width = map_width
        self.map_height = map_height 

    def update(self, palyer_centerx, palyer_centery , ):
        # 更新相机位置，使玩家保持在屏幕中央
        target_x = palyer_centerx - SCREEN_WIDTH // 2
        target_y = palyer_centery - SCREEN_HEIGHT // 2
        
        # 限制相机不超出地图边界
        self.x = max(0, min(target_x, self.map_width - SCREEN_WIDTH))
        self.y = max(0, min(target_y, self.map_height - SCREEN_HEIGHT))