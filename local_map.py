
from map import *

class local_map(Map):
    def __init__(self, screen, x = 0, y = 0, l = 40):
        Map.__init__(self, screen, x, y, l)

    def wait(self):
        while True:
            for event in pygame.event.get():
                #根据所处state及键盘输入判断state变化
                #初始：0 选定操作对象； 1 选定移动地点； 2 行动； 3 攻击； 4 治疗； 5 使用； 6 交换
                if event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        if self.state in (0,1,11):
                            self.move('left')
                        elif self.state == 3:
                            self.to_attack = (self.to_attack + 1) % len(self.attackable)
                            self.now[0] = self.attackable[self.to_attack].loc_x
                            self.now[1] = self.attackable[self.to_attack].loc_y
                        elif self.state == 4:
                            self.to_treat = (self.to_treat + 1) % len(self.treatable)
                            self.now[0] = self.treatable[self.to_treat].loc_x
                            self.now[1] = self.treatable[self.to_treat].loc_y
                        elif self.state == 6:
                            self.to_exchange = (self.to_exchange + 1) % len(self.exchangeable)
                            self.now[0] = self.exchangeable[self.to_exchange].loc_x
                            self.now[1] = self.exchangeable[self.to_exchange].loc_y
                        elif self.state == 7:
                            if self.exg_tag == 1:
                                self.exg_sel[1] = -1
                                self.exg_sel[0] = 0
                            self.exg_tag = 0
                            
                            
                    elif event.key == K_d:
                        if self.state in (0,1,11):
                            self.move('right')
                        elif self.state == 3:
                            self.to_attack = (self.to_attack + 1) % len(self.attackable)
                            self.now[0] = self.attackable[self.to_attack].loc_x
                            self.now[1] = self.attackable[self.to_attack].loc_y
                        elif self.state == 4:
                            self.to_treat = (self.to_treat + 1) % len(self.treatable)
                            self.now[0] = self.treatable[self.to_treat].loc_x
                            self.now[1] = self.treatable[self.to_treat].loc_y
                        elif self.state == 6:
                            self.to_exchange = (self.to_exchange + 1) % len(self.exchangeable)
                            self.now[0] = self.exchangeable[self.to_exchange].loc_x
                            self.now[1] = self.exchangeable[self.to_exchange].loc_y
                        elif self.state == 7:
                            if self.exg_tag == 0:
                                self.exg_sel[0] = -1
                                self.exg_sel[1] = 0
                            self.exg_tag = 1
                        
                    elif event.key == K_w:
                        if self.state in (0,1,11):
                            self.move('up')
                        elif self.state == 2:
                            self.selection = (self.selection - 1)% 5
                            while self.action[self.selection] == 0:
                                self.selection = (self.selection - 1)% 5
                        elif self.state == 3:
                            self.to_attack = (self.to_attack + 1) % len(self.attackable)
                            self.now[0] = self.attackable[self.to_attack].loc_x
                            self.now[1] = self.attackable[self.to_attack].loc_y
                        elif self.state == 4:
                            self.to_treat = (self.to_treat + 1) % len(self.treatable)
                            self.now[0] = self.treatable[self.to_treat].loc_x
                            self.now[1] = self.treatable[self.to_treat].loc_y
                        elif self.state == 5:
                            self.select_thing = (self.select_thing - 1)% len(self.per_sel.backpack)
                        elif self.state == 6:
                            self.to_exchange = (self.to_exchange + 1) % len(self.exchangeable)
                            self.now[0] = self.exchangeable[self.to_exchange].loc_x
                            self.now[1] = self.exchangeable[self.to_exchange].loc_y
                        elif self.state == 7:
                            self.exg_sel[self.exg_tag] = (self.exg_sel[self.exg_tag] - 1) % 5
                            
                    elif event.key == K_s:
                        if self.state in (0,1,11):
                            self.move('down')
                        elif self.state == 2:
                            self.selection = (self.selection + 1)% 5
                            while self.action[self.selection] == 0:
                                self.selection = (self.selection + 1)% 5
                        elif self.state == 4:
                            self.to_treat = (self.to_treat + 1) % len(self.treatable)
                            self.now[0] = self.treatable[self.to_treat].loc_x
                            self.now[1] = self.treatable[self.to_treat].loc_y
                        elif self.state == 3:
                            self.to_attack = (self.to_attack + 1) % len(self.attackable)
                            self.now[0] = self.attackable[self.to_attack].loc_x
                            self.now[1] = self.attackable[self.to_attack].loc_y
                        elif self.state == 5:
                            self.select_thing = (self.select_thing - 1)% len(self.per_sel.backpack)
                        elif self.state == 6:
                            self.to_exchange = (self.to_exchange + 1) % len(self.exchangeable)
                            self.now[0] = self.exchangeable[self.to_exchange].loc_x
                            self.now[1] = self.exchangeable[self.to_exchange].loc_y
                        elif self.state == 7:
                            self.exg_sel[self.exg_tag] = (self.exg_sel[self.exg_tag] + 1) % 5

                    elif event.key == K_j:
                        if(self.state == 0):
                            #temp = 0
                            for i in [0,1]:
                                for index in self.list_person[i]:
                                    if index.loc_x == self.now[0] and index.loc_y == self.now[1]:
                                        self.per_sel = index
                                        self.state = 1
                                        self.get_ari(self.now[0], self.now[1], index.arrive)
                                    
                        elif self.state == 1:
                            if self.per_sel.finished == 1or self.per_sel.camp != self.camp:
                                self.show()
                                continue
                            if (self.now[0],self.now[1]) not in self.arrival:
                                self.show()
                                continue
                            flag = 0
                            for i in [0,1]:
                                for index in self.list_person[i]:
                                    if index.loc_x == self.now[0] and index.loc_y == self.now[1]:
                                        if index.uuid !=self.per_sel.uuid:
                                            flag = 1
                                            break
                            if flag == 0:
                                self.to[0] = self.now[0]
                                self.to[1] = self.now[1]
                                self.show()
                                self.state = 2
                                self.set_attackable()
                                self.action = [0,0,1,0,1]
                                if len(self.attackable) != 0:
                                    self.action[0] = 1
                                for index in self.list_person[self.per_sel.camp]:
                                    if self.neighbor(self.to[0], self.to[1], index):
                                        self.action[3] = 1
                                        if index.blood < index.max_blood and \
                                           self.per_sel.equip != None and\
                                           '杖' in self.per_sel.weapons and \
                                           self.per_sel.equip.type == '杖':
                                            self.action[1] = 1
                                        break
                                            
                                if self.action[0] == 1:        
                                    self.selection = 0
                                elif self.action[1] == 1:
                                    self.selection = 1
                                else:
                                    self.selection = 2
                                #self.action(self.per_sel)
                            else:
                                print("此处有人")
                        #攻击
                        elif self.state == 2 and self.selection == 0:
                            if self.action[0] == 0:
                                raise AssertionError("错误，不能攻击")
                            self.state = 3
                            self.now[0] = self.attackable[self.to_attack].loc_x
                            self.now[1] = self.attackable[self.to_attack].loc_y
                        #治疗
                        elif self.state == 2 and self.selection == 1:
                            self.set_treatable()
                            self.state = 4
                            self.now[0] = self.treatable[self.to_treat].loc_x
                            self.now[1] = self.treatable[self.to_treat].loc_y
                        #物品
                        elif self.state == 2 and self.selection == 2:
                            self.state = 5
                            if len(self.per_sel.backpack) != 0:
                                self.select_thing = 0
                        #交换
                        elif self.state == 2 and self.selection == 3:
                            self.set_exchangeable()
                            self.state = 6
                            self.now[0] = self.exchangeable[self.to_exchange].loc_x
                            self.now[1] = self.exchangeable[self.to_exchange].loc_y
                        #待机
                        elif self.state == 2 and self.selection == 4:
                            self.per_sel.move(self.to[0], self.to[1])
                            self.per_sel.finished = 1
                            self.per_sel = None
                            self.person_finish()
                            
                            

                        #state2中尚未完成的部分
                            
                        elif self.state == 3:
                            self.per_sel.move(self.to[0], self.to[1])
                            #print(self.check_attack(self.attackable[self.to_attack], self.attackable[self.to_attack]))
                            fight.fight(self.screen, self.per_sel, self.attackable[self.to_attack], \
                                        self.check_attack(self.attackable[self.to_attack], self.attackable[self.to_attack]))
                            self.check_alive(self.per_sel)
                            self.check_alive(self.attackable[self.to_attack])
                            self.now[0] = self.to[0]
                            self.now[1] = self.to[1]
                            self.per_sel.finished = 1
                            self.per_sel = None
                            self.person_finish()

                        elif self.state == 4:
                            self.per_sel.move(self.to[0], self.to[1])
                            self.treatable[self.to_treat].blood += self.per_sel.strength + self.per_sel.equip.damage
                            if self.treatable[self.to_treat].blood > self.treatable[self.to_treat].max_blood:
                                self.treatable[self.to_treat].blood = self.treatable[self.to_treat].max_blood
                            self.per_sel.equip.endure -= 1
                            self.per_sel.check_equip()
                            self.per_sel.to_equip()
                            self.now[0] = self.to[0]
                            self.now[1] = self.to[1]
                            self.per_sel.finished = 1
                            self.per_sel = None
                            self.person_finish()
                            

                        elif self.state == 5:
                            if self.select_thing == -1:
                                continue
                            if self.per_sel.backpack[self.select_thing].type in self.per_sel.weapons:
                                temp = self.per_sel.backpack[0]
                                self.per_sel.backpack[0] = self.per_sel.backpack[self.select_thing]
                                self.per_sel.backpack[self.select_thing] = temp
                                self.select_thing = 0
                                self.per_sel.to_equip()
                                self.action = [0,0,1,0,1]
                                for index in self.list_person[self.per_sel.camp]:
                                    if self.neighbor(self.to[0], self.to[1], index):
                                        self.action[3] = 1
                                        if index.blood < index.max_blood and \
                                           self.per_sel.equip != None and\
                                           '杖' in self.per_sel.weapons and \
                                           self.per_sel.equip.type == '杖':
                                            self.action[1] = 1
                                        break
                                self.set_attackable()
                                if len(self.attackable) != 0:
                                    self.action[0] = 1
                                self.move_again = 1
                                
                            elif self.per_sel.backpack[self.select_thing].type == '药':
                                if self.per_sel.blood == self.per_sel.max_blood:
                                    self.show()
                                    continue
                                self.per_sel.move(self.to[0], self.to[1])
                                self.per_sel.backpack[self.select_thing].endure -= 1
                                self.per_sel.blood += self.per_sel.backpack[self.select_thing].damage
                                if self.per_sel.blood > self.per_sel.max_blood:
                                    self.per_sel.blood = self.per_sel.max_blood
                                if self.per_sel.backpack[self.select_thing].endure <= 0:
                                    self.per_sel.backpack.remove(self.per_sel.backpack[self.select_thing])
                                self.now[0] = self.to[0]
                                self.now[1] = self.to[1]
                                self.per_sel.finished = 1
                                self.per_sel = None
                                self.person_finish()

                        elif self.state == 6:
                            self.state = 7
                            self.exg_tag = 0
                            self.exg_sel = [0,-1]

                        elif self.state == 7:
                            person = (self.per_sel, self.exchangeable[self.to_attack])
                            if self.exg_sel[1 - self.exg_tag] == -1:
                                if len(person[self.exg_tag].backpack) >  self.exg_sel[self.exg_tag]:
                                    self.exg_sel[1 - self.exg_tag] = 0
                                    self.exg_tag = 1 - self.exg_tag                          
                            else:
                                if len(person[self.exg_tag].backpack) >  self.exg_sel[self.exg_tag]:
                                    temp = person[self.exg_tag].backpack[self.exg_sel[self.exg_tag]]
                                    person[self.exg_tag].backpack[self.exg_sel[self.exg_tag]] = \
                                                         person[1 - self.exg_tag].backpack[self.exg_sel[1 - self.exg_tag]]
                                    person[1 - self.exg_tag].backpack[self.exg_sel[1 - self.exg_tag]] = temp
                                else:
                                    temp = person[1 - self.exg_tag].backpack[self.exg_sel[1 - self.exg_tag]]
                                    del person[1 - self.exg_tag].backpack[self.exg_sel[1 - self.exg_tag]]
                                    person[self.exg_tag].backpack.append(temp)
                                person[0].to_equip()
                                person[1].to_equip()
                                self.action = [0,0,1,0,1]
                                for index in self.list_person[self.per_sel.camp]:
                                    if self.neighbor(self.to[0], self.to[1], index):
                                        self.action[3] = 1
                                        if index.blood < index.max_blood and \
                                           self.per_sel.equip != None and\
                                           '杖' in self.per_sel.weapons and \
                                           self.per_sel.equip.type == '杖':
                                            self.action[1] = 1
                                        break
                                self.set_attackable()
                                if len(self.attackable) != 0:
                                    self.action[0] = 1
                                self.move_again = 1
                                self.exg_sel[self.exg_tag] = 0
                                self.exg_sel[1 - self.exg_tag] = -1
                                
                            
                        
                    elif event.key == K_k:
                        if(self.state == 1):
                            self.state = 0
                            self.now[0] = self.per_sel.loc_x
                            self.now[1] = self.per_sel.loc_y
                            self.per_sel = None
                            self.arrival = []
                        elif(self.state == 11):
                            self.state = 0
                            self.per_sel = None
                            self.arrival = []
                        elif(self.state == 2):
                            if self.move_again == 1:
                                self.state = 0
                                self.per_sel.move(self.to[0], self.to[1])
                                self.per_sel.finished = 1
                                self.per_sel = None
                                self.selection = 0
                                self.arrival = []
                                self.attackable = []
                                self.to_attack = 0
                                self.check_finished()
                                self.move_again = 0
                                self.show()
                                continue 
                            self.state = 1
                            self.attackable = []
                            self.now[0] = self.to[0]
                            self.now[1] = self.to[1]
                            self.to = [0,0]
                        elif(self.state == 3):
                            self.state = 2
                            self.now[0] = self.per_sel.loc_x
                            self.now[1] = self.per_sel.loc_y
                            self.to_attack = 0
                        elif(self.state == 4):
                            self.state = 2
                            self.now[0] = self.per_sel.loc_x
                            self.now[1] = self.per_sel.loc_y
                            self.to_attack = 0
                        elif self.state == 5:
                            self.state = 2
                            self.select_thing = -1
                        elif self.state == 6:
                            self.state = 2
                            self.to_exchange = 0
                            self.exchangeable = []
                        elif self.state == 7:
                            if self.exg_sel[1 - self.exg_tag] != -1:
                                self.exg_sel[self.exg_tag] = -1
                                self.exg_tag = 1 - self.exg_tag
                            else:
                                self.exg_tag = 0
                                self.exg_sel = [0,-1]
                                self.state = 6

                    elif event.key == K_i:
                        index = self.here(self.now[0], self.now[1])
                        if index != None:
                            if index.equip != None:
                                print(index.equip.name)
                            else :
                                print('None')
                    elif event.key == K_p:
                        self.save('haha3')
                        
                    elif event.key == K_q:
                        print("alive")
                        print(self.state)

                    self.show()
                    
                            
        

