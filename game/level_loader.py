import json
import os
from config import *

class LevelLoader:
    def __init__(self):
        pass
        
    def load_level(self, level_name):
        """从JSON文件加载关卡"""
        filepath = os.path.join(LEVELS_PATH, f"{level_name}.json")
        
        with open(filepath, 'r') as f:
            level_data = json.load(f)
            
        return level_data
    
    def save_level(self, level_name, level_data):
        """保存关卡到JSON文件"""
        filepath = os.path.join(LEVELS_PATH, f"{level_name}.json")
        
        with open(filepath, 'w') as f:
            json.dump(level_data, f, indent=2)

