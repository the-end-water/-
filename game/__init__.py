"""
游戏核心模块
包含游戏场景、玩家、实体等核心类
"""

# from .scene import GameScene
from .player import Player
# from .entities import Enemy, NPC, Item
from .camera import Camera
from .level_loader import LevelLoader

# 定义包的公共接口
__all__ = [
    'GameScene',
    'Player', 
    'Enemy',
    'NPC',
    'Item',
    'Camera',
    'LevelLoader'
]

# 包版本
__version__ = "1.0.0"