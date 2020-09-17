
import pygame,pyautogui
import time,os,datetime
from GUIHandler import *

# --- main_old ---



# - init -
GUI=GUIHandler()
running = True
msg_dic={}
start_time = time.perf_counter()
starting_second=datetime.datetime.now().second
starting_minute=datetime.datetime.now().minute
starting_hour=datetime.datetime.now().hour

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                pass
                
        elif event.type == pygame.MOUSEMOTION:
            pass
    
    if time.perf_counter()-start_time>5:
        current=pyautogui.position()
        pyautogui.click(x=2260,y=315)
        pyautogui.click(x=2260,y=335)
        pyautogui.click(x=current[0],y=current[1])
        #pyautogui.moveTo(1900, 320, duration = 0.5) 
        start_time=time.perf_counter()
   
    # - draws (without updates) -
    
    try:
        files=os.listdir("livechats")
        for file in files:
            f=open("livechats\\"+file+"\\meeting_saved_chat.txt","r+",encoding="utf-8")
            for line in f:
                hour=line.split(":")[0]
                minute=line.split(":")[1]
                sec=line.split(":")[2][:2]
                msg=line.split(":")[3].strip()
                user=line.split("From")[1].split(":")[0].strip()
                msg_id=hour+":"+minute+":"+sec+":"+user
                if int(hour)*3600+int(minute)*60+int(sec)>=starting_hour*3600+starting_minute*60+starting_second:
                    if msg_id not in msg_dic.keys():
                        flt=Float_Message(msg,msg_id)
                        msg_dic[msg_id]=flt
            f.close()
    except:
        pass
    #GUI.screen.blit(GUI.background,(0,0))

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
    if len(msgs)>0:
        float_display(msgs)
    GUI.clock.tick(FPS)

# - end -

pygame.quit()
