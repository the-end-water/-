import pygame
import json
import os
import sys
from config import *

class LoadingAnimation:
    def __init__(self):
        self.progress = 0
        self.is_loading = False
        self.loading_start_time = 0
        self.loading_duration = 2000  # 加载时间2秒
        
    def start_loading(self):
        self.is_loading = True
        self.progress = 0
        self.loading_start_time = pygame.time.get_ticks()
        
    def update(self):
        if self.is_loading:
            elapsed = pygame.time.get_ticks() - self.loading_start_time
            self.progress = min(elapsed / self.loading_duration, 1.0)
            
            if self.progress >= 1.0:
                self.is_loading = False
                return True  # 加载完成
        return False
    
    def draw(self, screen):
        if not self.is_loading:
            return
            
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 250))  # 半透明黑色
        screen.blit(overlay, (0, 0))
        
        # 绘制加载框
        loading_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50, 300, 130)
        pygame.draw.rect(screen, WHITE, loading_rect)
        pygame.draw.rect(screen, BLACK, loading_rect, 4)
        
        # 绘制进度条
        bar_rect = pygame.Rect(SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2, 260, 20)
        pygame.draw.rect(screen, BLUE, bar_rect)
        
        progress_width = int(260 * self.progress)
        progress_rect = pygame.Rect(SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2, progress_width, 20)
        pygame.draw.rect(screen, BLUE, progress_rect)
        
        # 绘制加载文字
        font = pygame.font.SysFont('simhei', 36)
        text = font.render("加载中...", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        
        # 绘制百分比
        percent_text = font.render(f"{int(self.progress * 100)}%", True, BLACK)
        screen.blit(percent_text, (SCREEN_WIDTH//2 - percent_text.get_width()//2, SCREEN_HEIGHT//2 + 30))
