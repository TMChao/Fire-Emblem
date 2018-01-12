import pygame
import uuid
import pickle

class thing:
    def __init__(self, name, type, endure, damage, hit = 0):
        self.name = name
        self.endure = endure
        self.type = type
        self.damage = damage
        self.hit = hit
        

class person:
    def __init__(self, name, job, camp = 2, backpack = [], loc_x = None, loc_y = None, blood = 0, finished = 0):
        self.name = name
        self.face = pygame.image.load('头像\\' + self.name + ".png").convert()
        self.face_temp = self.face
        live = 1
        self.blood = blood
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.job = job
        self.attr_init(job)
        self.camp = camp
        self.uuid = uuid.uuid1()
        self.finished = finished
        self.backpack = backpack
        self.to_equip()
                
                

    def to_equip(self):
        self.equip = None
        for i in range(len(self.backpack)):
            if self.backpack[i].type in self.weapons:
                self.equip = self.backpack[i]
                temp = self.backpack[i]
                self.backpack[i] = self.backpack[0]
                self.backpack[0] = temp
                break

    def check_equip(self):
        if self.equip == None:
            return False
        if self.equip.endure <= 0:
            del self.backpack[0]
            self.equip = None
            return False
        return True

    def attr_init(self, job):
        if(job == '剑士'):
            self.weapons = '剑'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [16,4,9,9,2,0,5]
        elif(job == '剑圣'):
            self.weapons = '剑',
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [21,6,12,13,3,2,6]
        elif(job == '重甲'):
            self.weapons = '枪',
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [17,5,2,0,9,0,4]
        elif(job == '将军'):
            self.weapons = '枪',
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [23,8,4,3,13,3,4]
        elif(job == '战士'):
            self.weapons = '斧',
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [20,5,2,4,2,0,5]
        elif(job == '勇士'):
            self.weapons = '斧',
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [28,8,5,6,5,0,5]
        elif(job == '弓箭手'):
            self.weapons = '弓',
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [18,4,3,3,3,0,5]

        elif(job == '狙击手'):
            self.weapons = '弓',
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [21,7,10,5,5,2,5]
        elif(job == '轻骑士'):
            self.weapons = '剑','枪'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [20,5,2,5,5,0,6]
        elif(job == '弓骑士'):
            self.weapons = '剑','弓'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [21,7,6,7,6,3,7]
        elif(job == '重骑士'):
            self.weapons = '剑','枪','斧'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [25,8,4,3,10,2,6]
        elif(job == '圣骑士'):
            self.weapons = '剑','枪'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [23,7,5,7,8,5,8]
        elif(job == '魔法师'):
            self.weapons = '理'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [16,1,3,2,2,4,5]
        elif(job == '修道士'):
            self.weapons = '光'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [18,1,1,2,1,5,5]
        elif(job == '牧师'):
            self.weapons = '杖'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [16,1,2,2,0,6,5]
        elif(job == '巫师'):
            self.weapons = '杖'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [16,2,1,2,2,4,5]
        elif(job == '贤者'):
            self.weapons = '理','光'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [20,5,4,4,5,5,5]
        elif(job == '司祭'):
            self.weapons = '光','杖'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [21,4,4,4,3,8,5]
        elif(job == '德鲁伊'):
            self.weapons = '理','暗'
            self.attribute = [self.max_blood,\
                              self.strength,\
                              self.skill,\
                              self.speed,
                              self.defence,\
                              self.magic_defence,\
                              self.arrive]\
                              = [19,6,3,4,4,6,5]
        
            

    def set(self, loc_x, loc_y):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.blood = self.max_blood

    def move(self, loc_x, loc_y):
        self.loc_x =loc_x
        self.loc_y = loc_y
        

class save_person:
    def __init__(self, person):
        self.name = person.name
        self.blood = person.blood
        self.job = person.job
        self.camp = person.camp
        self.loc_x = person.loc_x
        self.loc_y = person.loc_y
        self.finished = person.finished
        self.backpack = []
        for index in person.backpack:
            self.backpack.append(index)

#pygame.init()
#erk = person('Eirika','剑圣',0)
#if erk.equip == None:
#    print('xx')
#s1 = thing('必杀刃', '剑', 20, 15)
#print(s1.type)

if __name__ == "__main__":
    screen = pygame.display.set_mode((400,300))
    pygame.init()
    f = open('存档\\temp.save', 'wb')
    erk = person('艾瑞珂','剑士',0, backpack = [thing('圣药', '药', 1, 100), \
                                            thing('必杀刃', '剑', 20, 7, 100)], \
                        loc_x = 1, loc_y = 1, blood = 20)
    erk_save = save_person(erk)
    pickle.dump(erk_save, f)
    f.close()
    f = open('存档\\temp.save', 'rb')
    s1 = pickle.load(f)
    s2 = person(s1.name, s1.job, s1.camp, backpack = s1.backpack, loc_x = s1.loc_x, loc_y = s1.loc_y, blood = s1.blood)
    f.close()
    print(s2.blood)
    
    


