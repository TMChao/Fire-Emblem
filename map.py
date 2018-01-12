import pygame
import sys
import uuid
import os
import pickle
from pygame.locals import *
import person
import fight

class Map:
    def __init__(self, screen, x = 0, y = 0, l = 40):
        self.screen = screen
        self.map = []
        
        self.width = 0
        self.height = 0
        self.now = [x, y]
        self.NW = self.NW_x, self.NW_y = 0, 0
        self.length = l
        self.font = pygame.font.SysFont('simhei', self.length//2)
        self.font_small = pygame.font.SysFont('simhei', self.length//3)
        self.to = [0,0]
        self.action = [0, 0, 1, 0, 1]

        self.round = 0
        self.camp = 0
        self.finish = 0

        #列表
        self.arrival = []
        self.attackable = []
        self.exchangeable = []
        self.treatable = []
        self.list_person = [[],[],[]]
        self.list_land = []

        # tag
        self.state = 0
        self.per_sel = None
        self.to_attack = 0
        self.to_exchange = 0
        self.to_treat = 0
        self.selection = 0
        self.select_thing = -1
        self.exg_tag = 0
        self.exg_sel = [0,-1]
        self.move_again = 0

        # 地形
        self.land_color()

    def land_color(self):
        temp = pygame.image.load('地形\\平原.png').convert()
        temp = pygame.transform.scale(temp, (self.length, self.length))
        self.list_land.append((temp,'平原',1))
        temp = pygame.image.load('地形\\丘陵.png').convert()
        temp = pygame.transform.scale(temp, (self.length, self.length))
        self.list_land.append((temp,'丘陵',2))
        self.arrive = pygame.Surface((self.length, self.length))
        self.arrive.fill((50,255,50)) 
        self.arrive.set_alpha(100)
        self.camp0 = pygame.Surface((self.length, self.length))
        self.camp0.fill((50,50,255)) 
        self.camp0.set_alpha(150)
        self.camp1 = pygame.Surface((self.length, self.length))
        self.camp1.fill((255,50,50)) 
        self.camp1.set_alpha(150)
        self.bg_camp = [self.camp0, self.camp1]
        self.bg_finished = pygame.Surface((self.length, self.length))
        self.bg_finished .fill((50,50,50)) 
        self.bg_finished .set_alpha(150)

    def save(self, name):
        if os.path.exists('存档\\save_list.fe') and os.path.getsize('存档\\save_list.fe') != 0:
            fp = open('存档\\save_list.fe',"rb")
            save_list = pickle.load(fp)
            fp.close()
            flag = 0
            for index in save_list:
                if name == index[0]:
                    #弹出是否覆盖，处理
                    flag = 1
            if flag == 0:
                save_list.append((name,0))
        else:
            save_list = [(name,0)]
        fp = open('存档\\save_list.fe',"wb")
        pickle.dump(save_list, fp)
        fp.close()

        fp = open('存档\\' + name + '.save', 'wb')
        save_person = [[],[],[]]
        for i in [0,1,2]:
            for index in self.list_person[i]:
                save_person[i].append(person.save_person(index))
        save_state = [self.round, self.camp]
        pickle.dump([self.map,save_person, save_state], fp)
        fp.close()

    def load_(self, name):
        if os.path.exists('存档\\save_list.fe') == False:
            raise AssertionError("存档列表失联")
        if os.path.getsize('存档\\save_list.fe') == 0:
            raise AssertionError("无存档")
        fp = open('存档\\save_list.fe',"rb")
        save_list = pickle.load(fp)
        fp.close()
        for index in save_list:
            print(index)

    def load(self, name):
        fname = '存档\\' + name + '.save'
        if os.path.exists(fname) == False:
            raise AssertionError('无此存档')
        if os.path.getsize('存档\\save_list.fe') == 0:
            raise AssertionError("存档内容丢失")
        fp = open(fname, 'rb')
        data = pickle.load(fp)
        fp.close()
        self.map = data[0]
        self.width = len(data[0][0])
        self.height = len(data[0])
        load_person = data[1]
        for i in [0,1,2]:
            self.list_person[i] = []
            for index in load_person[i]:
                temp = person.person(index.name, index.job, index.camp, \
                                  backpack = index.backpack, loc_x = index.loc_x, \
                                  loc_y = index.loc_y, blood = index.blood, finished = index.finished)
                temp.face_temp = pygame.transform.scale(temp.face,(self.length*2//3,self.length*2//3))
                self.list_person[i].append(temp)
        self.round = data[2][0]
        self.camp = data[2][1]
            
        
        
    def map_read(self, name):
        fp = open(name,"r")
        read_map = fp.readlines()
        self.width = int(read_map[0])
        self.height = int(read_map[1])
        map_ = []
        for index_ in read_map[2:len(read_map)]:
            temp = []
            for index in index_:
                if index == '\n': continue
                temp.append(int(index))
            if len(temp) != self.width:
                raise AssertionError("地图宽度出错")
            map_.append(temp)
        if len(map_) != self.height:
            raise AssertionError("地图高度出错")
        self.map = map_

    #根据state判断显示
    #初始：0 选定操作对象：1 选定移动地点：2 攻击：3 物品：4 交换：5
    def show(self):         
        self.now_rect = pygame.Rect((self.now[1] - self.NW_y) * self.length - 1, \
                                    (self.now[0] - self.NW_x) * self.length - 1, \
                                    self.length + 2, self.length + 2)
        for i in range(self.height):
            for j in range(self.width):
                    self.screen.blit(self.list_land[self.map[i][j]][0],(self.length * (j-self.NW_y), self.length * (i-self.NW_x)))        
        for index in self.list_person[self.camp]:
            if index.finished == 0:
                self.screen.blit(self.bg_camp[self.camp], (self.length * (index.loc_y-self.NW_y),\
                                                   self.length * (index.loc_x-self.NW_x)))
            else:
                self.screen.blit(self.bg_finished, (self.length * (index.loc_y-self.NW_y),\
                                                   self.length * (index.loc_x-self.NW_x)))
            self.screen.blit(index.face_temp, (self.length * (index.loc_y-self.NW_y) + self.length//6,
                                                self.length * (index.loc_x-self.NW_x) + self.length//6))
        for index in self.list_person[1 - self.camp]:
            self.screen.blit(self.bg_camp[1 - self.camp], (self.length * (index.loc_y-self.NW_y),\
                                                           self.length * (index.loc_x-self.NW_x)))
            self.screen.blit(index.face_temp, (self.length * (index.loc_y-self.NW_y) + self.length//6,
                                               self.length * (index.loc_x-self.NW_x) + self.length//6))   
        for i in range(self.height):
            for j in range(self.width):
                if i == self.now[0] and j == self.now[1]:
                    pygame.draw.rect(self.screen,[0,0,0],self.now_rect,1)

        if self.finish == 1:
            flag = pygame.Surface((self.screen.get_width(), self.screen.get_height()//5))
            flag.fill((0,0,0))
            self.screen.blit(flag, (0, self.screen.get_height() * 2//5))
            self.screen.blit(self.font.render('回合结束',True, (255,255,255)), \
                    (self.screen.get_width()//2 - self.length, self.screen.get_height()*9//20))
            self.finish = 0

        if self.state != 2:
            window = pygame.Surface((self.length*2, self.length*2))
            if self.now[1] - self.NW_y >= (self.screen.get_width()//self.length\
                                           - self.NW_y)//2:
                if self.now[0] - self.NW_x >= (self.screen.get_height()//self.length\
                                               - self.NW_x)//2:
                    point = (0, 0)
                else:
                    point = (0, self.screen.get_height() - self.length*2)
            else:
                if self.now[0] - self.NW_x >= (self.screen.get_height()//self.length\
                                               - self.NW_x)//2:
                    point = (self.screen.get_width() - 2*self.length, 0)
                else:
                    point = (self.screen.get_width() - 2*self.length, \
                             self.screen.get_height() - 2*self.length)
            window.fill([200, 160, 100])
            self.screen.blit(window, point)
            index = self.here(self.now[0], self.now[1])
            pygame.display.flip()
            if index != None:
                self.screen.blit(self.font.render(index.name, True, (0,0,0)), \
                                 (point[0] + self.length - len(index.name) * self.length//4, \
                                  point[1] + self.length//4))
                self.screen.blit(self.font.render(str(index.blood), True, (0,0,0)), \
                                 (point[0] + self.length//2 - len(str(index.blood)) * self.length//8, \
                                  point[1] + self.length*5//4))
                self.screen.blit(self.font.render('/', True, (0,0,0)), \
                                 (point[0] + self.length * 7//8, \
                                  point[1] + self.length*5//4))
                self.screen.blit(self.font.render(str(index.max_blood), True, (0,0,0)), \
                                 (point[0] + self.length*3//2 - len(str(index.max_blood)) * self.length//8, \
                                  point[1] + self.length*5//4))
            else:
                self.screen.blit(self.font.render(self.list_land[self.map[self.now[0]][self.now[1]]][1], True, (0,0,0)), \
                                 (point[0] + self.length*2//4, point[1] + self.length*3//4))
                

        if self.state == 1:
            if self.per_sel.finished == 1:
                for index in self.arrival:
                    self.screen.blit(self.bg_finished,(self.length * (index[1] - self.NW_y),\
                                                       self.length * (index[0] - self.NW_x)))
            elif self.per_sel.camp != self.camp:
                for index in self.arrival:
                    self.screen.blit(self.bg_camp[self.per_sel.camp],(self.length * (index[1] - self.NW_y),\
                                                                           self.length * (index[0] - self.NW_x)))
            else:
                for index in self.arrival:
                    self.screen.blit(self.bg_camp[self.camp],(self.length * (index[1] - self.NW_y),\
                                                                   self.length * (index[0] - self.NW_x)))
            


        elif self.state == 2:
            if self.to[1] - self.NW_y >= (self.width - self.NW_y)//2:
                point = (self.length/2, self.length/2)
            else:
                point = (self.screen.get_width() - 5*self.length/2, self.length/2)
                
            num = sum(self.action)
            self.screen.blit(self.bg_camp[self.camp], (self.length * (self.to[1] - self.NW_y),\
                                    self.length * (self.to[0] - self.NW_x)))
            lable = ['攻击','治疗','物品','交换','待机']
            window = pygame.Surface((self.length*2, self.length*num))
            window.fill([200, 160, 100])
            self.screen.blit(window, point)
            i_ = 0
            for i in range(5):
                if self.action[i] == 1:
                    self.screen.blit(self.font.render(lable[i] , True, (0,0,0)), \
                                (point[0] + self.length//2, point[1] + self.length/4 + i_ * self.length))
                    if(i == self.selection):
                        rect = (point[0], point[1] + i_ * self.length, self.length*2, self.length)
                        pygame.draw.rect(self.screen, [0,0,0], rect, 1)
                    i_ += 1

        elif self.state == 3:
            if self.per_sel.loc_x != self.now[0] and self.per_sel.loc_y != self.now[1]:
                self.screen.blit(self.bg_camp[self.camp], (self.length * (self.to[1] - self.NW_y),\
                                        self.length * (self.to[0] - self.NW_x)))

        elif self.state == 4:
            self.screen.blit(self.bg_camp[self.camp], (self.length * (self.to[1] - self.NW_y),\
                                    self.length * (self.to[0] - self.NW_x)))

        elif self.state == 5:
            if self.to[1] - self.NW_y >= (self.width - self.NW_y)//2:
                point = (self.length/2, self.length/2)
            else:
                point = (self.screen.get_width() - 7*self.length/2, self.length/2)
            window = pygame.Surface((self.length*3, self.length*6))
            window.fill([200, 160, 100])
            self.screen.blit(window, point)
            self.screen.blit(self.font.render(self.per_sel.name, True, (0,0,0)), \
                                 (point[0] + self.length*3//2 - len(self.per_sel.name) * self.length//4, \
                                  point[1] + self.length//4))
            if self.select_thing != -1:
                rect = (point[0], point[1] + self.select_thing * self.length + self.length, self.length*3, self.length)
                pygame.draw.rect(self.screen, [255,255,255], rect, 1)
                i = 1
                for index in self.per_sel.backpack:
                    self.screen.blit(self.font_small.render(index.name, True, (0,0,0)), \
                                     (point[0] + self.length - len(index.name) * self.length//6, \
                                      point[1] + self.length//3 + self.length*i))
                    self.screen.blit(self.font_small.render(str(index.endure), True, (0,0,0)), \
                                     (point[0] + self.length*5//2 - len(str(index.endure)) * self.length//12, \
                                      point[1] + self.length//3 + self.length*i))
                    i += 1

        elif self.state == 6:
            self.screen.blit(self.bg_camp[self.camp], (self.length * (self.to[1] - self.NW_y),\
                                    self.length * (self.to[0] - self.NW_x)))
        
        elif self.state == 7:
            point = ((self.screen.get_width()//2 - 4 * self.length, \
                      self.screen.get_height()//2 - 4 * self.length),\
                     (self.screen.get_width()//2 + self.length, \
                      self.screen.get_height()//2 - 4 * self.length))
            window = pygame.Surface((self.length*3, self.length*6))
            window.fill([200, 160, 100])
            self.screen.blit(window, point[0])
            self.screen.blit(window, point[1])
            person = (self.per_sel, self.exchangeable[self.to_attack])
            for i in (0,1):
                self.screen.blit(self.font.render(person[i].name, True, (0,0,0)), \
                                 (point[i][0] + self.length*3//2 - len(person[i].name) * self.length//4, \
                                  point[i][1] + self.length//4))
                j = 1
                for index in person[i].backpack:
                    self.screen.blit(self.font_small.render(index.name, True, (0,0,0)), \
                                     (point[i][0] + self.length - len(index.name) * self.length//6, \
                                      point[i][1] + self.length//3 + self.length*j))
                    self.screen.blit(self.font_small.render(str(index.endure), True, (0,0,0)), \
                                     (point[i][0] + self.length*5//2 - len(str(index.endure)) * self.length//12, \
                                      point[i][1] + self.length//3 + self.length*j))
                    j += 1
                if self.exg_sel[i] != -1:
                    rect = (point[i][0], point[i][1] + (self.exg_sel[i] + 1) * self.length,\
                            self.length*3, self.length)
                    pygame.draw.rect(self.screen, [255,255,255], rect, 1)
                    
                    

            
        pygame.display.flip()

    def s_move(self, to):
        if(to == 'left'):
            if(self.NW_y > 0):
                self.NW_y -= 1
        if(to == 'right'):
            if(self.NW_y < self.width - self.screen.get_width()/40):
                self.NW_y += 1
        if(to == 'up'):
            if(self.NW_x > 0):
                self.NW_x -= 1
        if(to == 'down'):
            if(self.NW_x < self.height - self.screen.get_height()/40):
                self.NW_x += 1

    def move(self, to):
        
        if(to == 'left'):
            if(self.now[1] > 0):
                self.now[1] -= 1
                if(self.now[1] < self.NW_y ):
                    self.s_move('left')
        if(to == 'right'):
            if(self.now[1] < self.width - 1):
                self.now[1] += 1
                if(self.now[1] >= self.NW_y +  self.screen.get_size()[0]/40):
                    self.s_move('right')
        if(to == 'up'):
            if(self.now[0] > 0):
                self.now[0] -= 1
                if(self.now[0] < self.NW_x):
                    self.s_move('up')
        if(to == 'down'):
            if(self.now[0] < self.height - 1):
                self.now[0] += 1
                if(self.now[0] >= self.NW_x +  self.screen.get_size()[1]/40):
                    self.s_move('down')
                    
    def seac(self, x, y, distance):
        if x > 0 and distance[x - 1][y] > distance[x][y] + self.list_land[self.map[x - 1][y]][2]:
            distance[x - 1][y] = distance[x][y] + self.list_land[self.map[x - 1][y]][2]
            self.seac(x - 1, y, distance)

        if x < self.height - 1 and distance[x + 1][y] > distance[x][y] + self.list_land[self.map[x + 1][y]][2]:
            distance[x + 1][y] = distance[x][y] + self.list_land[self.map[x + 1][y]][2]
            self.seac(x + 1, y, distance)

        if y > 0 and distance[x][y - 1] > distance[x][y] + self.list_land[self.map[x][y - 1]][2]:
            distance[x][y - 1] = distance[x][y] + self.list_land[self.map[x][y - 1]][2]
            self.seac(x, y - 1, distance)

        if y < self.width - 1 and distance[x][y + 1] > distance[x][y] + self.list_land[self.map[x][y + 1]][2]:
            distance[x][y + 1] = distance[x][y] + self.list_land[self.map[x][y + 1]][2]
            self.seac(x, y + 1, distance)


    
    def get_ari(self, x, y, step):
        distance = []
        for i in range(self.height):
            temp = []
            for j in range(self.width):
                temp.append(1000)
            distance.append(temp)
        distance[x][y] = 0
        self.seac(x, y, distance)
        for i in range(self.height):
            for j in range(self.width):
                if(distance[i][j] <= step):
                    self.arrival.append((i,j))

    def set_person(self, person, x, y):
        flag = 0
        for i in [0,1]:
            for index in self.list_person[i]:
                if index.loc_x == x and index.loc_y == y:
                    flag = 1
                    break
        if flag == 0:
            person.set(x, y)
            person.face_temp = pygame.transform.scale(person.face,(self.length*2//3,self.length*2//3))
            self.list_person[person.camp].append(person)
        else:
            raise AssertionError("此处已有人")
        
    def neighbor(self, x, y, person2):
        if x == person2.loc_x and y == person2.loc_y + 1 or\
           x == person2.loc_x and y == person2.loc_y - 1 or\
           x == person2.loc_x + 1 and y == person2.loc_y or\
           x == person2.loc_x - 1 and y == person2.loc_y :
            return True
        else:
            return False

    def here(self, x, y, camp = -1):
        if camp == -1:
            for index in self.list_person[0]:
                if index.loc_x == x and index.loc_y == y:
                    return index
            for index in self.list_person[1]:
                if index.loc_x == x and index.loc_y == y:
                    return index
            return None
        for index in self.list_person[camp]:
            if index.loc_x == x and index.loc_y == y:
                return index
        return None

    #def show_action(self, action, point, select):
    
    def check_attack(self, person, index):
        if person.equip == None:
            return 
        if person.equip.type in ['剑','枪','斧']:
            if abs(index.loc_x - self.to[0]) + abs(index.loc_y - self.to[1]) == 1:
                return True
            return False
                                
        elif person.equip.type == '弓':
            if abs(index.loc_x - self.to[0]) + abs(index.loc_y - self.to[1]) == 2:
                return True
            return False
                    
        elif person.equip.type in ['理','暗','光']:
            if abs(index.loc_x - self.to[0]) + abs(index.loc_y - self.to[1]) <= 2:
                return True
            return False

    def set_attackable(self):
        person = self.per_sel
        self.attackable = []
        if person.equip == None:
            return 
        for index in self.list_person[1 - person.camp]:
            
            if self.check_attack(person, index) == True:
                self.attackable.append(index)
                if index.loc_x < self.NW_x:
                    self.NW_x = index.loc_x
                elif(index.loc_x >= self.NW_x + self.screen.get_size()[1]//40):
                    self.NW_x = index.loc_x - self.screen.get_size()[1]//40 + 1
                if index.loc_y < self.NW_y:
                    self.NW_y = index.loc_y
                elif(index.loc_y >= self.NW_y + self.screen.get_size()[0]//40):
                    self.NW_y = index.loc_y - self.screen.get_size()[0]//40 + 1

    def set_exchangeable(self):
        for index in self.list_person[self.per_sel.camp]:
            if self.per_sel.uuid == index.uuid:
                continue
            if self.neighbor(self.to[0], self.to[1], index):
                self.exchangeable.append(index)

    def set_treatable(self):
        for index in self.list_person[self.per_sel.camp]:
            if self.per_sel.uuid == index.uuid:
                continue
            if index.blood != index.max_blood and self.neighbor(self.to[0], self.to[1], index):
                self.treatable.append(index)
                                

    def check_alive(self, person):
        if(person.blood == 0):
            self.list_person[person.camp].remove(person)
            if person == self.attackable[self.to_attack]:
                del self.attackable[self.to_attack]
            return False
        return True

    def check_finished(self):
        tag = 0
        for index in self.list_person[self.camp]:
            if index.finished == 0:
                tag = 1
        if tag == 0:
            for index in self.list_person[self.camp]:
                index. finished = 0
            self.camp = 1 - self.camp
            if self.camp == 1:
                self.round += 1
            self.finish = 1

    def person_finish(self):
        self.state = 0
        self.selection = 0
        self.arrival = []
        self.move_again = 0
        self.check_finished()

    def wait(self):
        pass

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    pygame.display.set_caption("map")
    map1 = Map(screen)
    map1.save('haha')
    map1.load('haha')



        


    


