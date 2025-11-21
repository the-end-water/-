import cv2
import pygame
import numpy as np
import sys
import threading
import time

class VideoPlayer:
    def __init__(self , start_time , final_time , file_path , screen_width ,screen_height):
        pygame.init()
        self.cap = None # 视频主体
        self.first_play = False
        self.playing = True
        self.current_time = 0

        self.start_time = start_time
        self.end_time = final_time
        self.start_frame = None
        self.end_frame= None

        self.width = None
        self.height = None
        self.total_time = 0  # 视频总时长
        self.total_frames = 0 # 视频总共帧数 = 视频总时长 * FPS
        self.fps = 0  # 视频帧率

        self.screen = None
        self.clock = pygame.time.Clock()

        self.load_video(file_path)

    def load_video(self, video_path):
        """加载视频文件"""
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            return False
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.total_time = self.total_frames / self.fps
        
        # 获取视频尺寸
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 初始化Pygame窗口
        # self.screen = pygame.display.set_mode((width, height))
        # pygame.display.set_caption("视频播放器")

        self.start_frame = int(self.start_time * self.fps)
        self.end_frame = int(self.end_time * self.fps)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)
        
        # print(f"视频加载成功: {video_path}")
        # print(f"视频时长: {self.end_time:.2f}秒")
        return True

    def play_video(self):
        """播放视频"""
        self.first_play = True
        # self.playing = True
        
        
        # while self.playing:
        #     ret, frame = self.cap.read()
        #     if not ret:
        #         break

        #     current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        #     if current_frame > end_frame:
        #         break
                
        #     # 将OpenCV的BGR格式转换为RGB
        #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     # 将numpy数组转换为Pygame表面
        #     frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
        #     # 显示帧
        #     self.screen.blit(frame_surface, (0, 0))
        #     pygame.display.flip()
        #     # 控制帧率
        #     self.clock.tick(self.fps)
        #     # 处理事件
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.playing = False
        #         elif event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_ESCAPE:
        #                 self.playing = False
        
        # self.playing = False
    
    def stop_video(self):
        """停止播放"""
        self.playing = False
    
    def close(self):
        """释放资源"""
        if self.cap:
            self.cap.release()
        pygame.quit()

