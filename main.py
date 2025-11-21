import pygame
import json
import os
import sys
import cv2
import numpy as np
from config import *
from game.player import Player
from game.camera import Camera
from game.dialog import *
from game.entities import NPC
from game.map_change_animation import LoadingAnimation
from game.video_player import VideoPlayer
from game.button import *
from graphics.tilesets import Map
from graphics.character import *
from graphics.map_video import *

# 初始化Pygame
pygame.init()
# 初始化字体模块
pygame.font.init()
# 初始化混音器
pygame.mixer.init()

class Game:
    def __init__(self):
        # *****************加载基本参数*****************
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG Game")
        self.clock = pygame.time.Clock()
        self.running = True
        # 游戏状态
        self.current_screen = COVER_SCREEN
        # 创建开始按钮
        self.start_button = Button(SCREEN_WIDTH//2 - 100, 400, 200, 60, "开始游戏", SAND_YELLOW, GREEN)

        # *****************加载地图*****************
        self.maps = maps
        self.map_birth_pos_list = [MAP_1_BIRTH_POS,MAP_2_BIRTH_POS,MAP_3_BIRTH_POS,MAP_4_BIRTH_POS,MAP_5_BIRTH_POS,
                                   MAP_6_BIRTH_POS,MAP_7_BIRTH_POS,MAP_8_BIRTH_POS,MAP_9_BIRTH_POS,MAP_10_BIRTH_POS,]
        self.current_map_index = 0
        self.map = self.maps[self.current_map_index]
        self.switching_map = False
        
        # *****************创建视频播放*****************
        self.current_video = None
        self.video_index = 0
        self.video_list = video_list

        # *****************创建对话框*****************
        self.dialogbox = DialogBox()
        self.dbox  = DBox(dialogue_text,width=SCREEN_WIDTH,height=SCREEN_HEIGHT-200)
        self.show_dialogue = True
        # *****************创建地图切换动画*****************
        self.loading_animation = LoadingAnimation()

        # *****************创建相机*****************
        self.camera = Camera(self.map.map_width, self.map.map_height,0,0)

        # *****************创建玩家（注意COL，ROW，SPEED，MOVE）*****************
        self.player = Player(BIRTH_POS[0], BIRTH_POS[1], MAIN_ANIMATION_IMAGE_PATH, MAIN_DIALOGUE)

        # *****************创建NPC*****************
        self.map_npc = map_npc
        self.npc_list = self.map_npc[self.map]
        '''
        # 创建游戏所有对象类
        '''
        self.group =pygame.sprite.Group()
        self.group.add(self.player)
        for npc in self.npc_list:
            self.group.add(npc)

    def get_current_map(self):
        return self.maps[self.current_map_index]
    
    def check_transition(self):
        current_map = self.get_current_map()
        player_rect = self.player.rect 
        
        for i, zone in enumerate(current_map.transition_zones):
            if player_rect.colliderect(zone):
                self.switch_to_next_map()
                # 删除当前地图的NPC
                for npc in self.map_npc[self.map]:
                    self.group.remove(npc)
                # 设置地图切换状态为“开始”
                self.switching_map = True

              
                return True
        return False
    
    def check_video(self):
        current_map = self.get_current_map()
        player_rect = self.player.rect 
        self.current_video = self.video_list[self.video_index]

        for i, zone in enumerate(current_map.video_zones):
            if player_rect.colliderect(zone):
               
                if not self.current_video.first_play:
                 
                    self.current_video.play_video()

                return True
        return False

    def complete_map_switch(self):
        # 切换到下一张地图
        self.current_map_index = (self.current_map_index + 1) % len(self.maps)
        self.video_index = (self.video_index + 1) % len(self.video_list)
        self.player.rect.x = self.map_birth_pos_list[self.current_map_index][0]
        self.player.rect.y = self.map_birth_pos_list[self.current_map_index][1]
        # 添加下一张地图的NPC
        for npc in self.map_npc[self.maps[self.current_map_index]]:
            self.group.add(npc)
        self.camera = Camera(self.maps[self.current_map_index].map_width, self.maps[self.current_map_index].map_height,0,0)
        self.show_dialogue = True  # 重置对话框状态
        self.dbox.index+=1
        self.dbox.visible = True  # 显示对话框

    def switch_to_next_map(self):
        # 开始加载动画
        self.loading_animation.start_loading()

    def draw(self):  
        #  ========== 绘制地图 ========== 
        self.map.draw(self.screen,self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)

        #  ========== 绘制玩家，NPC ========== 
        for sprite in self.group:
            self.screen.blit(sprite.image, 
                             (sprite.rect.x - self.camera.x, sprite.rect.y - self.camera.y))
        #  ========== 绘制玩家，NPC名字 ==========    
        for npc in self.npc_list:
            self.screen.blit(npc.name_text, 
                             (npc.rect.x - self.camera.x, npc.rect.y -npc.frame_height//2 - self.camera.y))
                            #  (npc.name_rect.centerx - self.camera.x, 
                            #   npc.name_rect.centery -npc.frame_height- self.camera.y))
            
        # ========== 绘制碰撞矩形（调试用） ========== 
        # for obj in self.map.collision_objects:
        #     pygame.draw.rect(self.screen, RED, 
        #                    (obj.x - self.camera.x, obj.y - self.camera.y, 
        #                     obj.width, obj.height), 1)
            
        # ========== 绘制对话框 ========== 
        self.dialogbox.draw(self.screen)
        self.dbox.draw(self.screen)
        # ========== 绘制过场动画 ========== 
        if self.switching_map:
            self.loading_animation.draw(self.screen)

        # ========== 绘制视频 ==========     
        if self.current_video.first_play and self.current_video.playing :
        
            ret, frame = self.current_video.cap.read()
            current_frame = self.current_video.cap.get(cv2.CAP_PROP_POS_FRAMES)
          
            if current_frame >= self.current_video.end_frame:
                self.current_video.playing = False
            # 将OpenCV的BGR格式转换为RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resize = cv2.resize(frame_rgb, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # 将numpy数组转换为Pygame表面
            frame_surface = pygame.surfarray.make_surface(np.rot90( np.flip(np.rot90(frame_resize),axis=1),k=2))
            # 显示帧
            self.screen.blit(frame_surface, (0, 0))

        pygame.display.flip()
    def draw_surface(self):
        # 绘制封面
        self.screen.blit(cover_image, (0, 0))
        
        # 绘制标题
        title_text = title_font.render("出埃及记", True, GOLD)
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        
        # 绘制按钮
        self.start_button.draw(self.screen)
        
        # 绘制提示文字
        hint_text = pygame.font.SysFont('simhei', 20).render("点击开始游戏按钮进入游戏", True, WHITE)
        self.screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, 500))
        pygame.display.flip()

    def run(self):
        pygame.mixer.music.load(MUSIC_PATH)
        # 设置循环播放（-1表示无限循环）
        pygame.mixer.music.play(-1)

        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.current_screen == COVER_SCREEN:
                    # 检查按钮点击
                    if self.start_button.is_clicked(mouse_pos, event):
                        self.current_screen = GAME_SCREEN
                        self.show_dialogue = True  # 重置对话框状态
                        self.dbox.visible = True  # 显示对话框
                        
                elif self.current_screen == GAME_SCREEN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        elif event.key == pygame.K_SPACE and self.show_dialogue:
                            # 按空格键隐藏对话框
                            self.dbox.hide()
                            self.show_dialogue = False
                            
                    # ************* 交互事件处理 ************* 
                    self.player.handle_event(event, 
                                            npcs=self.npc_list, 
                                            objects=[], 
                                            dialogBox=self.dialogbox)
                    
            # 更新按钮悬停状态
            if self.current_screen == COVER_SCREEN:
                self.start_button.check_hover(mouse_pos)

            if self.current_screen == COVER_SCREEN:
                self.draw_surface()
            elif self.current_screen == GAME_SCREEN:
                #  ************* 更新当前地图，以及地图内加载的NPC类别 ************* 
                self.map =  self.maps[self.current_map_index]
                self.npc_list = self.map_npc[self.map]
                
                
                # ************* 开始更新玩家，相机，NPC，地图状态，同时检查是否传送 *************
                self.player.update(collision_objects = self.map.collision_objects,
                                map_width= self.map.map_width,
                                map_height= self.map.map_height)
                
                for npc in self.npc_list:
                    npc.update()
            
                self.camera.update(self.player.rect.centerx,self.player.rect.centery)
                self.check_transition()
                self.check_video()
                self.draw()

                # ************* 绘制加载动画（如果有） *************
                if self.switching_map:
                    if self.loading_animation.update():
                        self.switching_map = False
                        self.complete_map_switch()
                # ************* 绘制加载动画（如果有） *************

            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # 确保有地图文件
    game = Game()
    game.run()
