import pygame
import sys
from config import *
pygame.init()
# 字体
title_font = pygame.font.SysFont('simhei', 64, bold=True)
button_font = pygame.font.SysFont('simhei', 36)

# 游戏界面背景
game_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
game_background.fill((60, 30, 30))
    
# 加载封面图片
cover_image = pygame.image.load("other_resource/surface.jpg")
cover_image = pygame.transform.scale(cover_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 创建封面元素
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=15)
        
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False
    
