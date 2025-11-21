import pygame
import json
import os
import sys
from config import *
from game import player
import random
# 初始化Pygame
pygame.init()
# 字体
title_font = pygame.font.SysFont('simhei', 64, bold=True)
button_font = pygame.font.SysFont('simhei', 36)
dialogue_font = pygame.font.SysFont('simhei', 24)

class DialogBox:
    def __init__(self):
        self.visible = False
        self.text = ""
        self.npc = None
        self.box_rect = pygame.Rect(50, 400, 700, 150)
        self.name = None
        
    def show(self, npc):
        self.visible = npc.is_interacting
        self.npc = npc
        self.text = npc.current_dialogue
        self.name = npc.name

    def hide(self):
        self.visible = False
        self.npc = None
        
    def next_text(self):
        if self.npc and not self.npc.next_dialog():
            self.hide()
        else:
            self.text = self.npc.dialog[self.npc.dialog_index]
        
    def draw(self,screen):
        if self.visible :
            # 绘制对话框背景
            pygame.draw.rect(screen, SAND_YELLOW, self.box_rect)
            pygame.draw.rect(screen, DARK_GOLD, self.box_rect, 4)
            
            # 绘制文本
            font_system = pygame.font.SysFont('simhei', 16)
            text_surface = font_system.render(self.text, True,BROWN)
            screen.blit(text_surface, (self.box_rect.x + 10, self.box_rect.y + 40))
            
            # 绘制提示继续的文本
            font_system_1 = pygame.font.SysFont('simhei', 16)
            continue_text = font_system_1.render("(按空格键继续...)", True,BROWN)
            screen.blit(continue_text, (self.box_rect.x + 10, self.box_rect.y + 100))

            # 绘制角色名字文本
            font_system_1 = pygame.font.SysFont('simhei', 24)
            continue_text = font_system_1.render(self.name, True,BROWN)
            screen.blit(continue_text, (self.box_rect.x + 10, self.box_rect.y +5))

# 创建对话框类
class DBox:
    def __init__(self, text, width=700, height=300):
        self.text = text
        self.width = width
        self.height = height
        self.rect = pygame.Rect((SCREEN_WIDTH - width) // 2, 50, width, height)
        self.visible = True
        self.index = 0

    def draw(self, surface):
        if not self.visible:
            return
            
        # 绘制对话框背景
        pygame.draw.rect(surface, BROWN, self.rect, border_radius=10)
        pygame.draw.rect(surface, SAND_YELLOW, self.rect, 3, border_radius=10)
        
        # 绘制文本（支持多行）
        lines = self.wrap_text(self.text[self.index], dialogue_font, self.width - 40)
        y_offset = self.rect.top + 300
        
        for line in lines:
            text_surf = dialogue_font.render(line, True, GOLD)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, y_offset))
            surface.blit(text_surf, text_rect)
            y_offset += 30
            
        # 绘制提示文字
        hint_text = dialogue_font.render("按空格键继续...", True, GOLD)
        hint_rect = hint_text.get_rect(center=(self.rect.centerx, self.rect.bottom - 25))
        surface.blit(hint_text, hint_rect)
        
    def wrap_text(self, text, font, max_width):
        """将文本换行以适应对话框宽度"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
    
    def hide(self):
        self.visible = False