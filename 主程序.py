import pygame
import sys
import os
import pickle
import map
import person
import fight
import socket
import local_map
import net_map
from pygame.locals import *


pygame.init()
size = width,height = 16, 12
length = 40
screen = pygame.display.set_mode([width*length, height*length])
pygame.display.set_caption("FE")
state = 0
selection = 0
label = []
font = pygame.font.SysFont('simhei', length)

background = pygame.transform.scale(pygame.image.load('主程序\\封面.jpg').convert(), \
                                    [width*length, height*length])
screen.blit(background,(0,0))
pygame.display.flip()

#
#map1 = map.Map(screen)
##map1.map_read("map_temp.txt")
#map1.load('haha2')

#pygame.display.flip()
##pygame.display.flip()
#map1.show()
#

def mainmenu(label):
    background = pygame.transform.scale(pygame.image.load('主程序\\主菜单.jpg').convert(), \
                                    [width*length, height*length])
    screen.blit(background,(0,0))
    temp = pygame.Surface((width*length//2, length))
    temp.fill((218,178,115))
    for i in range(len(label)):
        screen.blit(temp, (width*length//4, (height - len(label)*2 +1 + 4*i)*length//2))
        screen.blit(font.render(label[i], True, (255,255,255)),\
                    ((width - len(label[i]))*length//2,(height - len(label)*2 + 1 + 4*i)*length//2))
    pygame.draw.rect(screen, [0,0,0],\
                     (width*length//4,(height - len(label)*2 + 1 + 4*selection)*length//2,\
                     width*length//2, length), 3)
    pygame.display.flip()

def get_num(event):
    if event.key == K_0:
        return '0'
    elif event.key == K_1:
        return '1'
    elif event.key == K_2:
        return '2'
    elif event.key == K_3:
        return '3'
    elif event.key == K_4:
        return '4'
    elif event.key == K_5:
        return '5'
    elif event.key == K_6:
        return '6'
    elif event.key == K_7:
        return '7'
    elif event.key == K_8:
        return '8'
    elif event.key == K_9:
        return '9'
    elif event.key == K_PERIOD:
        return '.'
    else:
        return None

def init_map(map1):
    map1.map_read("map_temp.txt")
    erk = person.person('艾瑞珂','剑士',0, backpack = [person.thing('圣药', '药', 1, 100), \
                      person.thing('必杀刃', '剑', 20, 7, 100)])
    map1.set_person(erk,1,1)
    asl = person.person('阿斯雷','司祭',0, backpack = [person.thing('治疗之杖', '杖', 1, 5), \
                                                  person.thing('闪光', '光', 20, 5, 110)])
    map1.set_person(asl,1,5)
    lte = person.person('露忒','贤者',0, backpack = [person.thing('火球术', '理', 20, 6, 90)])
    map1.set_person(lte,1,3)
    lte = person.person('赛思','圣骑士',0, backpack = [person.thing('铁剑', '剑', 1, 5, 100),\
                                                  person.thing('铁之大剑', '剑', 20, 8, 85)])
    map1.set_person(lte,1,4)
    aml =person.person('艾米莉亚','将军',1, backpack = [person.thing('铁枪', '枪', 20, 6, 90)])
    map1.set_person(aml,6,5)
    flc =person.person('弗朗茨','重骑士',1, backpack = [person.thing('圣药', '药', 1, 100), person.thing('铁斧', '斧', 20, 7, 80)])
    map1.set_person(flc,5,6)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if state == 0:
                state = 1
                label = ('单人游戏','多人游戏')
                mainmenu(label)            
            else:
                if state == -1:
                    if event.key == K_j:
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((label[0] , 10021))
                            s.send('1'.encode())
                            if s.recv(1024).decode() == '2':
                                map1 = net_map.net_map(screen, sock = s, player = 0)
                                init_map(map1)
                                pygame.display.flip()
                                map1.show()
                                map1.wait()
                        except socket.gaierror:
                            #could not resolve
                            print ('Hostname could not be resolved. Exiting')
                            sys.exit()
                    else:
                        temp = get_num(event)
                        if temp != None:
                            label[0] += temp
                            mainmenu(label)
                if event.key == K_w:
                    selection = (selection - 1)%len(label)
                elif event.key == K_s:
                    selection = (selection + 1)%len(label)
                elif event.key == K_j:
                    if state == 1:
                        if selection == 0:
                            #state = 1.1
                            print('单人模式正在开发中，敬请期待')
                        elif selection == 1:
                            state = 1.2
                            label = ('热座模式','联网对战','返回上层')
                            selection = 0
                    elif state == 1.2:
                        if selection == 0:
                            state = 1.21
                            label = ('新游戏','读取存档','返回上层')
                            selection = 0
                        elif selection == 1:
                            state = 1.22
                            label = ('发起连接','等待连接')
                            selection = 0
                        else: 
                            state = 1
                            label = ('单人游戏','多人游戏')
                            selection = 0
                    elif state == 1.21:
                        if selection == 0:
                            map1 = local_map.local_map(screen)
                            init_map(map1)
                            pygame.display.flip()
                            map1.show()
                            map1.wait()
                            continue
                        elif selection == 1:
                            state = 1.212
                            selection = 0
                            if os.path.exists('存档\\save_list.fe') == False:
                                raise AssertionError("存档列表失联")
                            if os.path.getsize('存档\\save_list.fe') == 0:
                                raise AssertionError("无存档")
                            fp = open('存档\\save_list.fe',"rb")
                            save_list = pickle.load(fp)
                            fp.close()
                            label = []
                            for index in save_list:
                                label.append(index[0])
                            label.append('返回上层')
                        else:
                            state = 1.2
                            label = ('热座模式','联网对战','返回上层')
                            selection = 0
                    elif state ==1.212:
                        if selection < len(label) - 1:
                            map1 = local_map.local_map(screen)
                            map1.load(label[selection])
                            pygame.display.flip()
                            map1.show()
                            map1.wait()
                            continue
                        else:
                            state = 1.21
                            label = ('新游戏','读取存档','返回上层')
                            selection = 0

                    elif state == 1.22:
                        if selection == 0:
                            state = - 1
                            label = ['127.0.0.1','返回上级']
                        elif selection == 1:
                            state == 1.222
                            label = ('等待中……','返回上层')
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.bind(('127.0.0.1', 10021))
                            s.listen(1) 
                            sock, addr = s.accept()
                            if sock.recv(1024).decode() == '1':
                                sock.send('2'.encode())
                                print('已发送2')
                                map1 = net_map.net_map(screen, sock = sock, player = 1)
                                init_map(map1)
                                map1.show()
                                print('map.show()')
                                map1.wait()
                            

                    elif state == 1.222:
                        if selection == 1:
                            state = 1.22
                            label = ('发起连接','等待连接')
                            selection = 0
                            
                            
                            
                mainmenu(label)
                
                
            #        
            #map1.show()
        pygame.time.delay(30)


