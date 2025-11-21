import pygame
import json
import os
import sys
import cv2
import numpy as np
from config import *
from game.entities import NPC
from graphics.map_video import *
# 初始化Pygame
pygame.init()
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

npc_1 = NPC(780,550,
                         name=NPC_1_NAME, 
                         directions=DIRECTIONS,
                         cols=NPC_COLS,
                         rows=NPC_ROWS,
                         animation_paths=NPC_1_ANIMATION_IMAGE_PATH,
                         dialogues= NPC_1_DIALOGUE,
                         direction_cols=False)

npc_2 = NPC(880,650,
                         name='长老', 
                         directions=DIRECTIONS,
                         cols=NPC_COLS,
                         rows=NPC_ROWS,
                         animation_paths=NPC_2_ANIMATION_IMAGE_PATH,
                         dialogues= NPC_2_DIALOGUE,
                         direction_cols=False)
        
npc_3 = NPC(680,650,
                         name='公主', 
                         directions=DIRECTIONS,
                         cols=NPC_COLS,
                         rows=NPC_ROWS,
                         animation_paths=NPC_3_ANIMATION_IMAGE_PATH,
                         dialogues= NPC_3_DIALOGUE,
                         direction_cols=False)
        
npc_4 = NPC(680,650,name='士兵1',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,dialogues= NPC_4_DIALOGUE,direction_cols=False)
npc_4_1 = NPC(800,400,name='士兵2', directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,dialogues= NPC_4_DIALOGUE,direction_cols=False)
npc_4_2 = NPC(300,700,name='士兵3', directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,dialogues= NPC_4_DIALOGUE,direction_cols=False)
        
npc_5_1 = NPC(400,900,name='奴隶1', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_2 = NPC(250,900,name='奴隶2', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_3 = NPC(350,700,name='奴隶3', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_4 = NPC(280,800,name='奴隶4', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_5 = NPC(350,400,name='奴隶5', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_6 = NPC(1000,1000,name='奴隶6', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_7 = NPC(900,450,name='奴隶7', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_8 = NPC(700,260,name='奴隶8', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_5_0 = NPC(400,900,name='奴隶', 
                         directions=DIRECTIONS,cols=NPC_COLS,rows=NPC_ROWS,animation_paths=NPC_5_ANIMATION_IMAGE_PATH,direction_cols=False,dialogues=NPC_7_DIALOGUE)
        
npc_flame = NPC(800,500,
                         name='上帝', 
                         directions=FLAME_DIRECTIONS,
                         cols=FLAME_COLS,
                         rows=FLAME_ROWS,
                         animation_paths=FLAME_ANIMATION_IMAGE_PATH,
                         dialogues= NPC_5_DIALOGUE,
                         direction_cols=False)
        
npc_6_1 = NPC(200,230,name='民众1',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_6_ANIMATION_IMAGE_PATH,dialogues= NPC_6_DIALOGUE,direction_cols=False)
npc_6_2 = NPC(500,650,name='民众2',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_6_ANIMATION_IMAGE_PATH,dialogues= NPC_6_DIALOGUE,direction_cols=False)
npc_6_3 = NPC(900,430,name='民众3',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_6_ANIMATION_IMAGE_PATH,dialogues= NPC_6_DIALOGUE,direction_cols=False)
npc_6_4 = NPC(520,200,name='民众4',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_6_ANIMATION_IMAGE_PATH,dialogues= NPC_6_DIALOGUE,direction_cols=False)
npc_6_5 = NPC(520,800,name='民众5',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_6_ANIMATION_IMAGE_PATH,dialogues= NPC_6_DIALOGUE,direction_cols=False)

npc_7_1 = NPC(610,630,name='族人1',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_1,dialogues= NPC_7_DIALOGUE_1,direction_cols=False)
npc_7_2 = NPC(530,650,name='族人2',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_9,dialogues= NPC_7_DIALOGUE_3,direction_cols=False)
npc_7_3 = NPC(670,780,name='族人3',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_3,dialogues= NPC_7_DIALOGUE_4,direction_cols=False)
npc_7_4 = NPC(310,580,name='族人4',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_4,direction_cols=False)
npc_7_5 = NPC(800,850,name='族人5',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_5,direction_cols=False)
npc_7_6 = NPC(910,850,name='族人6',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_6,direction_cols=False)
npc_7_7 = NPC(1200,620,name='族人7',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_7,direction_cols=False)
npc_7_8 = NPC(1200,720,name='族人8',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_8,direction_cols=False)
npc_7_9 = NPC(510,730,name='亚伦',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_2,dialogues= NPC_7_DIALOGUE_2,direction_cols=False)
npc_7_10 = NPC(580,780,name='米利安',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_7,direction_cols=False)
        

npc_8 = NPC(780,550,
                         name='长子(新法老)', 
                         directions=DIRECTIONS,
                         cols=NPC_COLS,
                         rows=NPC_ROWS,
                         animation_paths=NPC_1_ANIMATION_IMAGE_PATH,
                         dialogues= NPC_8_DIALOGUE,
                         direction_cols=False)
        
npc_8_1 = NPC(700,700,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_2 = NPC(890,700,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_3 = NPC(700,780,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_4 = NPC(890,780,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_5 = NPC(700,860,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_6 = NPC(890,860,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_7 = NPC(700,940,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_8 = NPC(890,940,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_9 = NPC(700,1020,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_8_10 = NPC(890,1020,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
        

npc_9 = NPC(780,550,
                         name='长子（新法老）', 
                         directions=DIRECTIONS,
                         cols=NPC_COLS,
                         rows=NPC_ROWS,
                         animation_paths=NPC_1_ANIMATION_IMAGE_PATH,
                         dialogues= NPC_9_DIALOGUE,
                         direction_cols=False)
        
npc_9_1 = NPC(45,390,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_2 = NPC(115,390,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_3 = NPC(45,460,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_4 = NPC(115,460,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_5 = NPC(45,530,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_6 = NPC(115,530,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_7 = NPC(45,600,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_8 = NPC(115,600,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_9 = NPC(45,670,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_9_10 = NPC(115,670,name='士兵',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_4_ANIMATION_IMAGE_PATH,direction_cols=False)
npc_10 = NPC(190,560,
                         name='长子（新法老）', 
                         directions=DIRECTIONS,
                         cols=NPC_COLS,
                         rows=NPC_ROWS,
                         animation_paths=NPC_1_ANIMATION_IMAGE_PATH,
                         dialogues= NPC_9_DIALOGUE,
                         direction_cols=False)
npc_10_1 = NPC(700,380,name='族人1',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_1,direction_cols=False)
npc_10_2 = NPC(800,380,name='族人2',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_9,direction_cols=False)
npc_10_3 = NPC(660,450,name='族人3',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_3,direction_cols=False)
npc_10_4 = NPC(760,450,name='族人4',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_4,dialogues=NPC_10_DIALOGUE,direction_cols=False)
npc_10_5 = NPC(860,450,name='族人5',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_5,direction_cols=False)
npc_10_6 = NPC(600,640,name='族人6',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_6,direction_cols=False)
npc_10_7 = NPC(720,640,name='族人7',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_7,direction_cols=False)
npc_10_8 = NPC(840,640,name='族人8',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_8,direction_cols=False)
npc_10_9 = NPC(660,740,name='亚伦',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_2,dialogues= NPC_7_DIALOGUE_2,direction_cols=False)
npc_10_10 = NPC(760,740,name='米利安',directions=DIRECTIONS,
                         cols=NPC_COLS, rows=NPC_ROWS,animation_paths=NPC_7_ANIMATION_IMAGE_PATH_7,direction_cols=False)

map_npc =  {map_1:[ npc_1, npc_2, npc_3 ], # 宫殿
            
            map_2:[ npc_4, npc_4_1, npc_4_2, 
                    npc_5_1, npc_5_2, npc_5_3, npc_5_4,npc_5_5, npc_5_6, npc_5_7, npc_5_8  ],

            map_3:[ npc_flame  ],

            map_4:[ npc_6_1 ,npc_6_2 ,npc_6_3, npc_6_4, npc_6_5],

            map_5:[ npc_4, npc_4_1, npc_4_2, 
                    npc_5_0, npc_5_2, npc_5_3, npc_5_4,npc_5_5, npc_5_6, npc_5_7, npc_5_8  ],

            map_6:[npc_7_1, npc_7_2, npc_7_3, npc_7_4, npc_7_5, npc_7_6, npc_7_7, npc_7_8, npc_7_9, npc_7_10],# 埃及村落

            map_7:[npc_8_1,npc_8_2,npc_8_3,npc_8_4,npc_8_5, npc_8_6, npc_8_7, npc_8_8, npc_8_9, npc_8_10, npc_8 ],

            map_8:[npc_7_1, npc_7_2, npc_7_3, npc_7_4, npc_7_5, npc_7_6, npc_7_7, npc_7_8, npc_7_9, npc_7_10],

            map_9:[ npc_8_1,npc_8_2,npc_8_3,npc_8_4,npc_8_5, npc_8_6,npc_8_7,npc_8_8,npc_8_9,npc_8_10, npc_9 ],

            map_10:[npc_9_1,npc_9_2,npc_9_3,npc_9_4,npc_9_5, # 宫殿
                    npc_9_6,npc_9_7,npc_9_8,npc_9_9,npc_9_10,
                    npc_10, 
                    npc_10_1,npc_10_2,npc_10_3,npc_10_4,npc_10_5, # 宫殿
                    npc_10_6,npc_10_7,npc_10_8,npc_10_9,npc_10_10],
            }