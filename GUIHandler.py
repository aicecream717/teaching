'''
Created on Apr 8, 2020

@author: shan.jiang
'''
import pygame,pyautogui,os,random
import inputbox,time,pygame.font,fontlib
from pygame.locals import *
from numpy import sign

#Change thse parameters to fit to yoru screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 120

#Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255,   0,   0)
PINK  = (255, 170, 170)
ORANGE  = (255, 153, 51)

FPS = 60
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)   

class GUIHandler:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

class Float_Message():
    def __init__(self,msg,time_str):
        self.msg=msg
        self.time_str=time_str
        self.line=random.randint(0,3)
        self.indent=0
        self.x=SCREEN_WIDTH
        hour,minute,second,user=self.time_str.split(":")
        self.epoch=int(hour)*3600+int(minute)*60+int(second)
        self.user=user

def get_rect(x,y,width,height):
    rect=pygame.rect.Rect(x,y,width,height)
    return rect
    
def show_text(message="",size=80,location=(300,320),color=WHITE,outline=BLACK,flip=False,pause=0):
    bigfont = pygame.font.Font(None, size)
    text_img=fontlib.textOutline(bigfont, message, color, outline)
    screen.blit(text_img,location)
    if flip:
        pygame.display.flip()
        time.sleep(float(pause))



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background= pygame.transform.scale(pygame.image.load('black.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
stickers={}
files=os.listdir("images")
for file in files:
    image=pygame.transform.scale(pygame.image.load('images/'+file).convert_alpha(), (30,30))
    stickers[file.replace(".png","")]=image
pause_button=get_rect(0,0,30,120)      
pause_button_image=pygame.transform.scale(pygame.image.load('images/pause_button.png').convert_alpha(), (30,120))
        
        
        
            