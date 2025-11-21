import pygame
import json
import os
import sys
import cv2
import numpy as np
from config import *
from game.entities import NPC
from game.video_player import VideoPlayer
from game.button import *
from graphics.tilesets import Map

map_1 = Map(MAP_1,MAP_1_TRANSITION_ZONES,video_zones=MAP_1_VIDEO_ZONES) # 宫殿
map_2 = Map(MAP_2,MAP_2_TRANSITION_ZONES,video_zones=MAP_2_VIDEO_ZONES) # 采石场
map_3 = Map(MAP_3,MAP_3_TRANSITION_ZONES,video_zones=MAP_3_VIDEO_ZONES) # 西奈山
map_4 = Map(MAP_4,MAP_4_TRANSITION_ZONES,video_zones=MAP_4_VIDEO_ZONES) # 埃及城市
map_5 = Map(MAP_5,MAP_5_TRANSITION_ZONES,video_zones=MAP_5_VIDEO_ZONES) # 采石场
map_6 = Map(MAP_6,MAP_6_TRANSITION_ZONES,video_zones=MAP_6_VIDEO_ZONES) # 埃及村落
map_7 = Map(MAP_7,MAP_7_TRANSITION_ZONES,video_zones=MAP_7_VIDEO_ZONES) # 宫殿
map_8 = Map(MAP_8,MAP_8_TRANSITION_ZONES,video_zones=MAP_8_VIDEO_ZONES) # 埃及村落
map_9 = Map(MAP_9,MAP_9_TRANSITION_ZONES,video_zones=MAP_9_VIDEO_ZONES) # 宫殿
map_10= Map(MAP_10,MAP_10_TRANSITION_ZONES,video_zones=MAP_10_VIDEO_ZONES) # 红海

maps =[map_1,map_2,map_3,map_4,map_5,
        map_6,map_7,map_8,map_9,map_10]

video_1 = VideoPlayer(start_time=MAP_1_VIDEO_TIME[0],final_time=MAP_1_VIDEO_TIME[1],file_path=VIDEO_PATH, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
video_2 = VideoPlayer(start_time=MAP_2_VIDEO_TIME[0],final_time=MAP_2_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_3 = VideoPlayer(start_time=MAP_3_VIDEO_TIME[0],final_time=MAP_3_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_4 = VideoPlayer(start_time=MAP_4_VIDEO_TIME[0],final_time=MAP_4_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_5 = VideoPlayer(start_time=MAP_5_VIDEO_TIME[0],final_time=MAP_5_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_6 = VideoPlayer(start_time=MAP_6_VIDEO_TIME[0],final_time=MAP_6_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_7 = VideoPlayer(start_time=MAP_7_VIDEO_TIME[0],final_time=MAP_7_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_8 = VideoPlayer(start_time=MAP_8_VIDEO_TIME[0],final_time=MAP_8_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_9 = VideoPlayer(start_time=MAP_9_VIDEO_TIME[0],final_time=MAP_9_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)
video_10 = VideoPlayer(start_time=MAP_10_VIDEO_TIME[0],final_time=MAP_10_VIDEO_TIME[1],file_path=VIDEO_PATH,screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT)

video_list=[video_1, video_2, video_3, video_4,video_5,
            video_6, video_7, video_8, video_9,video_10]