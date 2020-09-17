'''
Created on Apr 8, 2020

@author: shan.jiang
'''
import pygame,pyautogui,os,random
import inputbox,time,pygame.font,fontlib
from pygame.locals import *
from numpy import sign

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255,   0,   0)
PINK  = (255, 170, 170)
ORANGE  = (255, 153, 51)
FPS = 60
x = 0
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)   
     
# --- main_old ---

# - init -
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background= pygame.transform.scale(pygame.image.load('black.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
   

class GUIHandler:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

class Float_Message():
    def __init__(self,msg,time_str):
        self.msg=msg
        self.time_str=time_str
        self.line=0
        self.indent=0
        hour,minute,second,user=self.time_str.split(":")
        self.epoch=int(hour)*3600+int(minute)*60+int(second)
        self.user=user
        
        
def show_text(message="",size=80,location=(300,320),color=WHITE,outline=BLACK,flip=False,pause=0):
    bigfont = pygame.font.Font(None, size)
    text_img=fontlib.textOutline(bigfont, message, color, outline)
    screen.blit(text_img,location)
    if flip:
        pygame.display.flip()
        time.sleep(float(pause))
        
def float_display(flts):
    pygame.event.pump()
    for flt in flts:
        flt.line=random.randint(0,3)
        flt.indent=(flt.epoch-flts[0].epoch)*100
    
    for k in range(100):
        screen.blit(background,(0,0))
        for flt in flts:
            show_text(flt.msg.lstrip("~"),size=50,location=(SCREEN_WIDTH*(1-k/50)+flt.indent,20*flt.line),flip=False)
        pygame.display.flip()
        time.sleep(0.1)
            
        
        
        
        
            