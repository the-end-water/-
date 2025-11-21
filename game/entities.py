import pygame
import json
import os
import sys
from config import *
from game import player
import random


class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, name,directions ,cols, rows ,animation_paths=None, dialogues=None,direction_cols = True):
        # 初始化字体模块
        pygame.font.init()
        """
        初始化NPC角色
        
        参数:
            x, y: 初始坐标
            name: NPC名称
            image_path: 静态NPC图片路径
            animation_paths: NPC动画路径字典
            dialogues: 对话内容字典
        """
        super().__init__()
        self.x = x
        self.y = y
        self.image = None
        self.images = None
        self.rect = None
        self.name = name
        self.name_text = pygame.font.SysFont('simhei', 18,bold=True).render(self.name, True, BROWN)
        self.name_rect = self.name_text.get_rect(center=(self.x , self.y))
   
        self.direction = directions[0] if len(directions)==1 else directions[2]

        # 动画更新参数
        self.index = 0
        self.counter = 0
        self.delay = 10

        self.animation_index = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        
        # 随机移动相关
        self.move_timer = 0
        self.random_move_interval = random.randint(2000, 5000)  # 2-5秒随机移动

        # 对话系统
        self.dialogues = dialogues
        self.current_dialogue_key = 'default'
        self.dialogue_index = 0
        '''
        ########## 交互状态和交互冷却 ##########
        '''
        self.is_interacting = False
        self.interaction_cooldown = 0
        
        # # 加载图像
        # if animation_paths:
        #     self.animations = {}
        #     for direction, paths in animation_paths.items():
        #         self.animations[direction] = [pygame.image.load(path).convert_alpha() for path in paths]
        #     self.image = self.animations[self.direction][self.animation_index]
        # elif image_path:
        #     self.image = pygame.image.load(image_path).convert_alpha()
        #     self.animations = None
        # else:
        #     # 默认图像
        #     self.image = pygame.Surface((32, 32))
        #     self.image.fill((0, 255, 0))  # 绿色矩形
        #     self.animations = None

        '''
        ############ 开始加载角色动画 ############
        '''
        # 创建总的角色动画帧图像集合
        self.images = {x:[] for x in directions}
        # 加载整张图片
        self.sprite_sheet = pygame.image.load(animation_paths).convert_alpha()
        # 计算每个动画帧的尺寸
        self.frame_width = self.sprite_sheet.get_width() // cols
        self.frame_height = self.sprite_sheet.get_height() // rows

        # 提取所有动画帧
        # 如果按照每一列为一个方向
        if direction_cols:
            for col in range(cols):
                for row in range(rows):
                    frame = self.sprite_sheet.subsurface(
                        col * self.frame_width,
                        row * self.frame_height,
                        self.frame_width,
                        self.frame_height
                    )
                    self.images[directions[col]].append(frame)
        # 每行是一个方向
        else:
            for col in range(cols):
                for row in range(rows):
                    frame = self.sprite_sheet.subsurface(
                        col * self.frame_width,
                        row * self.frame_height,
                        self.frame_width,
                        self.frame_height
                    )
                    self.images[directions[row]].append(frame)

        # self.rect = self.image.get_rect(center=(x, y))
        self.image = self.images[self.direction][self.index]
        self.rect = pygame.Rect(x, y, self.image.get_width(),self.image.get_height())
        # print(self.rect)
        # print(self.image.get_width(),self.image.get_height())
        # 碰撞检测相关
        self.collision_rect = pygame.Rect(0, 0, self.rect.width * 0.7, self.rect.height * 0.7)
        self.collision_rect.center = self.rect.center

    def update(self):
        """更新NPC状态"""
        # # 更新动画
        # if self.images:
        #     now = pygame.time.get_ticks()
        #     if now - self.last_update > 100:
        #         self.last_update = now
        #         self.animation_index = (self.animation_index + 1) % len(self.animations[self.direction])
        #         self.image = self.animations[self.direction][self.animation_index]
        # 人物动画帧更新
        if self.images :
            self.counter +=1
            if self.counter //self.delay ==1:
                self.counter %= 10
                self.index =(self.index + 1) % len(self.images[self.direction])
                self.image = self.images[self.direction][self.index]

        # 交互冷却
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= FPS  * 1000
        
        # # 随机移动（仅在未交互时）
        # if not self.is_interacting:
        #     self.move_timer += dt * 1000
        #     if self.move_timer >= self.random_move_interval:
        #         self._random_move()
        #         self.move_timer = 0
        #         self.random_move_interval = random.randint(2000, 5000)
    
    def interact(self):
        """与玩家交互"""
        if self.interaction_cooldown <= 0:
            self.is_interacting = True
            self.interaction_cooldown = 500  #
            self.get_next_dialogue()
    
    def get_next_dialogue(self):
        """获取下一句对话"""
        if self.current_dialogue_key in self.dialogues:
            # 获得当前条件(key)下的对话列表(dialogues)
            dialogues = self.dialogues[self.current_dialogue_key]

            # 按一次空格对话列表向后推进一次
            if self.dialogue_index < len(dialogues):
                self.current_dialogue = dialogues[self.dialogue_index]
                self.dialogue_index += 1

            # 对话列表推进到末尾，对话结束
            else:
                self.dialogue_index = 0
                self.is_interacting = False
           
    def set_dialogue(self, dialogue_key):
        """设置当前对话内容"""
        if dialogue_key in self.dialogues:
            self.current_dialogue_key = dialogue_key
            self.dialogue_index = 0
    
    def trigger_event(self, event_name):
        """触发事件，改变对话内容"""
        event_dialogue_key = f"event_{event_name}"
        if event_dialogue_key in self.dialogues:
            self.set_dialogue(event_dialogue_key)
    
    def render(self, screen):
        """渲染NPC"""
        # screen.blit(self.image, self.rect)
        
        # 如果正在交互，显示对话图标
        if self.is_interacting:
            font_system = pygame.font.SysFont('simhei', 36)
            text = font_system.render(self.current_dialogue, False, WHITE,BLACK)
            text_rect = text.get_rect(center=(self.rect.centerx + 50, self.rect.top + 50))
            screen.blit(text, text_rect)
         

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, name, image_path, interaction_texts=None):
        """
        初始化可交互物体
        
        参数:
            x, y: 初始坐标
            name: 物体名称
            image_path: 物体图片路径
            interaction_texts: 交互文本列表
        """
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
    
        # 加载图像
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            self.image = self.original_image
        except:
            # 如果加载失败，创建默认图像
            self.original_image = pygame.Surface((32, 32))
            self.original_image.fill((0, 0, 255))  # 蓝色矩形
            self.image = self.original_image
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # 交互系统
        self.interaction_texts = interaction_texts or [
            f"你检查了{name}",
            "这看起来很有趣",
            "也许以后会用得上"
        ]
        self.current_text_index = 0
        self.is_interacting = False
        self.interaction_cooldown = 0
        self.interaction_time = 0
        
        # 状态相关
        self.is_activated = False
        self.activation_count = 0
        
    def interact(self):
        """与物体交互"""
        if self.interaction_cooldown <= 0:
            self.is_interacting = True
            self.interaction_cooldown = 500
            self.interaction_time = 3000  # 显示文本3秒
            self.is_activated = True
            self.activation_count += 1
            
            text = self.get_next_interaction_text()
            return text
        return None
    
    def get_next_interaction_text(self):
        """获取交互文本"""
        if self.current_text_index < len(self.interaction_texts):
            text = self.interaction_texts[self.current_text_index]
            self.current_text_index += 1
            return text
        else:
            # 循环文本
            self.current_text_index = 0
            text = self.interaction_texts[self.current_text_index]
            self.current_text_index += 1
            return text
    
    def update(self, dt):
        """更新物体状态"""
        # 交互冷却
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= dt * 1000
        
        # 交互文本显示时间
        if self.is_interacting:
            self.interaction_time -= dt * 1000
            if self.interaction_time <= 0:
                self.is_interacting = False
    
    def set_interaction_texts(self, texts):
        """设置交互文本"""
        self.interaction_texts = texts
        self.current_text_index = 0
    
    def render(self, screen):
        """渲染物体"""
        screen.blit(self.image, self.rect)
        
        # 如果被激活过，可以改变外观
        if self.is_activated:
            # 添加发光效果或改变颜色
            highlight = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            highlight.fill((255, 255, 0, 50))  # 半透明黄色高光
            screen.blit(highlight, self.rect)
        
        # 如果正在交互，显示文本图标
        if self.is_interacting:
            font = pygame.font.Font(None, 24)
            text = font.render("!", True, (255, 255, 0))
            text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            screen.blit(text, text_rect)





