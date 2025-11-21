import pygame
import json
import os
import sys
from config import *
from game import player
from game.dialog import DialogBox

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, filenames ,dialogues):
        super().__init__()
        '''
        角色基本数值设置
            位置: x ,y
            速度: speed
            颜色: color
            朝向: direction
        '''
        self.x = x
        self.y = y
        self.name = '摩西'
        self.speed = PLAYER_SPEED
        self.color = BLUE
        self.direction = 'down'  # 初始面朝方向
        self.dialogues = dialogues
        self.dialogue_index =0
        self.current_dialogue = None
        self.current_dialogue_key = None
        self.interaction_cooldown = 0
        '''
        角色移动与交互设置
            是否运动: moving 
            交互范围: interact_range
            是否交互: is_interacting
        '''
         # 角色状态
        self.moving = False
        self.is_interacting = False
        self.interact_range = PLAYER_INTERACT_RANGE  # 交互范围
        '''
        角色动画播放设置
            是否运动: index 
            交互范围: counter
            是否交互: delay
        '''
        self.index = 0
        self.counter = 0
        self.delay = 10
        '''
        角色动画加载(动画状态和当前朝向以及是否运动有关)
            默认角色所有的朝向储存在一张图里面(filenames)
            各个朝向按照列分割：
            第一列：朝下
            第二列：朝左
            ...
        '''
        # 创建总的角色动画帧图像集合
        self.images = {x:[] for x in DIRECTIONS}
        # 加载整张图片
        self.sprite_sheet = pygame.image.load(filenames).convert_alpha()
        # 计算每个动画帧的尺寸
        self.frame_width = self.sprite_sheet.get_width() // COLS
        self.frame_height = self.sprite_sheet.get_height() // ROWS

        # 提取所有动画帧
        for col in range(COLS):
            for row in range(ROWS):
                frame = self.sprite_sheet.subsurface(
                    col * self.frame_width,
                    row * self.frame_height,
                    self.frame_width,
                    self.frame_height
                )
                self.images[DIRECTIONS[row]].append(frame)
                # self.images.append(frame)
        '''
        self.images
        {
            'up': [image1_1, image1_2, ...],
            'down': [image2_1, image2_2, ...],
            'left': [image3_1, image3_2, ...],
            'right': [image4_1, image5_2, ...]
        }
        '''
        '''
        # 角色的形状矩形
        '''
        self.image = self.images[self.direction][self.index]
        self.rect = pygame.Rect(x, y, self.image.get_width(),self.image.get_height())
        # print(self.image.get_width(),self.image.get_height())
        # 碰撞检测相关
        self.collision_rect = pygame.Rect(0, 0, self.rect.width * 0.7, self.rect.height * 0.7)
        self.collision_rect.center = self.rect.center
        
    # def update(self, dx, dy, collision_objects, screen, camera_x, camera_y):
    def update(self, collision_objects ,map_width ,map_height):
        '''
        角色状态更新, 包含2方面: 移动检测(提前预测碰撞), 动画更新
            collision_objects: (list[rect]) 当前地图里面的所有碰撞矩形
            必须是Tiled里面设置的名字是'collision'的对象层里面插入的碰撞矩形
        '''
        '''
        ######### 1-- 移动检测(提前预测碰撞) #########
        '''
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
            self.direction = 'left'
            self.moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
            self.direction = 'right'
            self.moving = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
            self.direction = 'up'
            self.moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            self.direction = 'down'
            self.moving = True
        else:
            self.moving = False

        # 尝试移动
        new_rect = self.rect.copy()
        new_rect.x += dx * self.speed
        new_rect.y += dy * self.speed
        
        # 检查碰撞
        collision = False
        for obj in collision_objects:
            if new_rect.colliderect(obj):
                collision = True
                break

        # 检查是否超出地图边界
        boundary = False

        if  new_rect.x > 0 and \
            new_rect.x < (map_width-self.frame_width) and \
            new_rect.y>0 and \
            new_rect.y < (map_height-self.frame_height):
            
            boundary = True

        # 更新对话冷却    
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= FPS  * 1000
            
        # 如果没有碰撞，则更新位置
        if not collision and boundary:
            self.rect = new_rect
        '''
        ######### 2-- 动画更新 #########
        '''
        # 人物动画帧更新
        if self.images and self.moving:
            self.counter +=1
            if self.counter //self.delay ==1:
                self.counter %= 10
                self.index =(self.index + 1) % len(self.images[self.direction])
                self.image = self.images[self.direction][self.index]
        elif self.images and not self.moving:
            # 静止时使用第一帧
            self.image = self.images[self.direction][0]
  
    def interact(self):
        """与玩家交互"""
        if self.interaction_cooldown <= 0:
            self.is_interacting = True
            self.interaction_cooldown = 500  
            self.get_next_dialogue()
    
    def get_next_dialogue(self):
        """获取下一句对话"""
        if self.current_dialogue_key in self.dialogues:
            # 获得当前条件(key)下的对话列表(dialogues)
            dialogues = self.dialogues[self.current_dialogue_key]
            # print(dialogues)
            # 按一次空格对话列表向后推进一次
            if self.dialogue_index < len(dialogues):
                self.current_dialogue = dialogues[self.dialogue_index]
                self.dialogue_index += 1
                if self.dialogue_index == len(dialogues):
                    self.dialogue_index = 0
                    self.is_interacting = False
              

            # 对话列表推进到末尾，对话结束
            else:
                self.dialogue_index = 0
                self.is_interacting = False

    def handle_event(self, event, npcs=None, objects=None ,dialogBox=None):
        """
        处理事件，特别是空格键交互
        
        参数:
            event: pygame事件
            npcs: NPC列表
            objects: 可交互物体列表
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # 检查面朝方向是否有NPC或可交互物体
            # self._get_target_position : 获取角色面朝方向的目标位置，用于交互检测
            target_pos = self._get_target_position()
            
            # 检查NPC
            if npcs:
                for npc in npcs:
                    # print(target_pos)
                    if npc.rect.collidepoint(target_pos):

                        self.current_dialogue_key = npc.name
                        # print('检测到NPC')
                        if not self.is_interacting:
                            '''
                            1-- npc交互，更新自己的下一句话
                                    首先检查自己的对话索引key
                                    基于索引key找到当前对话列表
                                    更新index更新当前语句
                            2-- dialogBox获得npc的当前语句，npc的名字，并且准备渲染
                            3-- 主角自己的交互状态设置为开启，方便后面对话
                            '''
                            npc.interact()
                            dialogBox.show(npc)
                            self.is_interacting = True

                            return
                        
                        elif self.is_interacting:
                            self.interact()
                            dialogBox.show(self)
                            self.is_interacting = False
                            return

            # 检查可交互物体
            if objects:
                for obj in objects:
                    if obj.rect.collidepoint(target_pos):
                        obj.interact()
                        self.is_interacting = True
                        return
                    
    def _get_target_position(self):
        """
        获取角色面朝方向的目标位置，用于交互检测
        """
        if self.direction == 'up':
            return (self.rect.centerx, self.rect.top - self.interact_range)
        elif self.direction == 'down':
            return (self.rect.centerx, self.rect.bottom + self.interact_range)
        elif self.direction == 'left':
            return (self.rect.left - self.interact_range, self.rect.centery)
        elif self.direction == 'right':
            return (self.rect.right + self.interact_range, self.rect.centery)
        
    
    # # 调试时使用    
    # def draw(self, screen, camera_x, camera_y):

    #     pygame.draw.rect(screen, self.color, 
    #                     (self.rect.x - camera_x, self.rect.y - camera_y, 
    #                      self.rect.width, self.rect.height))
        
    #     # 绘制玩家中心点（用于调试）
    #     pygame.draw.circle(screen, RED, 
    #                      (self.rect.centerx - camera_x, self.rect.centery - camera_y), 3)
