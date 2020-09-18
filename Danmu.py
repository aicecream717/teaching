'''author Shan Jiang --09-18-2020--'''



import pygame,pyautogui
import time,os,datetime
from GUIHandler import *

'''set the recording path variable to your Zoom recording destination'''
recording_path="C:\\Users\\jiangshan\Desktop\\Participation\\livechats"

def get_epoch(year,month,day,hour,minute,sec):
    value=0
    time_pieces=sec,minute,hour,day,month,year
    for i in range(6):
        value+=(60**i)*int(time_pieces[i])
    return value
    
# - init -
GUI=GUIHandler()
running = True
msg_dic={}
start_time = time.perf_counter()
starting_sec=datetime.datetime.now().second
starting_minute=datetime.datetime.now().minute
starting_hour=datetime.datetime.now().hour
starting_day=datetime.datetime.now().day
starting_month=datetime.datetime.now().month
starting_year=datetime.datetime.now().year



pause=False
while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pause_button.collidepoint(event.pos):
                    pause=not pause
                    

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                pass
                
        elif event.type == pygame.MOUSEMOTION:
            pass
    
    if not pause and time.perf_counter()-start_time>5:
        current=pyautogui.position()
        pyautogui.click(x=2250,y=315)
        pyautogui.click(x=2250,y=335)
        pyautogui.moveTo(current)
        #pyautogui.moveTo(1900, 320, duration = 0.5) 
        start_time=time.perf_counter()
   
    # - draws (without updates) -
    

    files=os.listdir(recording_path)
    for file in files:
        year,month,day=file.split(" ")[0].split("-")
        if get_epoch(year,month,day,0,0,0)>=get_epoch(starting_year,starting_month,starting_day,0,0,0):
            f=open(recording_path+"\\"+file+"\\meeting_saved_chat.txt","r+",encoding="utf-8")
            for line in f:
                if len(line.split(":"))>2:
                    hour=line.split(":")[0]
                    minute=line.split(":")[1]
                    sec=line.split(":")[2][:2]
                    msg=line.split(":")[3].strip()
                    user=line.split("From")[1].split(":")[0].strip()
                    msg_id=hour+":"+minute+":"+sec+":"+user
                    if get_epoch(year,month,day,hour,minute,sec)>=get_epoch(starting_year,starting_month,starting_day,starting_hour,starting_minute,starting_sec):
                        if msg_id not in msg_dic.keys():
                            flt=Float_Message(msg,msg_id)
                            msg_dic[msg_id]=flt
            f.close()

    #GUI.screen.blit(GUI.background,(0,0))

    '''
    msgs=[]
    current_sec=-1
    for k,v in msg_dic.items():
        if v.msg[0]!="~":
            sec=v.epoch
            if sec-current_sec<5 or current_sec==-1:
                msgs.append(v)
                msg_dic[k].msg="~"+v.msg
                current_sec=sec
            else:
                break
    if not pause and len(msgs)>0:
        float_display(msgs)
    '''
        
    screen.blit(background,(0,0))
    screen.blit(pause_button_image,(0,0))
    for msg_id,flt in msg_dic.items():
        if flt.x>-SCREEN_WIDTH:
            if flt.msg[0]=="\\":
                try:
                    image=stickers[flt.msg[1:]]
                    screen.blit(image,(flt.x,20*flt.line))
                except:
                    show_text(flt.msg,size=50,location=(flt.x,20*flt.line),flip=False)
            else:
                show_text(flt.msg,size=50,location=(flt.x,20*flt.line),flip=False)
            if not pause:
                flt.x-=5
    time.sleep(0.02)
    pygame.display.flip()
    GUI.clock.tick(FPS)

# - end -

pygame.quit()

    
    