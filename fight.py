import pygame
import person
import random

def refresh(screen, person1, person2, face1, face2, hurt1 = None, hurt2 = None):
    bg = (0,0,0)
    height = screen.get_height()
    width = screen.get_width()
    font = pygame.font.SysFont('simhei', width//24)
    font_small = pygame.font.SysFont('simhei', width//36)
    blood1 = pygame.Surface((person1.blood * width // 4 // person1.max_blood, \
                             height//16))
    blood1.fill((218,178,115))
    blood2 = pygame.Surface((person2.blood * width // 4 // person2.max_blood, \
                             height//16))
    blood2.fill((218,178,115))
    screen.fill(bg)
    screen.blit(face1, (width//8, height//4))
    screen.blit(face2, (width*5//8, height//4))
    pygame.draw.rect(screen, [218,178,115], \
                     [width//8, height*5//8,\
                      width//4, height//16], 3)
    pygame.draw.rect(screen, [218,178,115], \
                     [width*5//8, height*5//8,\
                      width//4, height//16], 3)
    screen.blit(blood1, (width//8, height*5//8))
    #print('blood1:',person1.blood)
    screen.blit(blood2, (width*5//8, height*5//8))
    hurt = (hurt1, hurt2)
    for i in (0, 1):
        if hurt[i] != None:
            print(i)
            if hurt[i] == -1:
                screen.blit(font.render('Miss',True, (255,255,255)), (width*(5+12*i)//24 , height//8))
            elif hurt[i] == 0:
                screen.blit(font.render('No Damage',True, (255,255,255)), (width*(1+3*i)//6 , height//8))
            else:
                screen.blit(font.render('-' + str(hurt[i]),True, (255,255,255)), \
                            (width*(1+2*i)//4 - width*len('-' + str(hurt[i]))//96 , height//8))
    
    if person1.equip != None:
        screen.blit(font.render(person1.equip.name,True, (255,255,255)), \
                    (width*5//24 - width*len(person1.equip.name)//48 , height*13//24))
        screen.blit(font.render(str(person1.equip.endure),True, (255,255,255)), \
                    (width//3 - width*len(str(person1.equip.endure))//48 , height*13//24))
    else:
        screen.blit(font.render('无装备',True, (255,255,255)), (width*3//16 , height*13//24))
        
    if person2.equip != None:
        screen.blit(font.render(person2.equip.name,True, (255,255,255)), \
                    (width*17//24 - width*len(person2.equip.name)//48 , height*13//24))
        screen.blit(font.render(str(person2.equip.endure),True, (255,255,255)), \
                    (width*5//6 - width*len(str(person2.equip.endure))//48 , height*13//24))
    else:
        screen.blit(font.render('无装备',True, (255,255,255)), (width*311//16 , height*13//24))
    screen.blit(font.render(str(person1.blood),True, (255,255,255)), (width//6 , height*3//4))
    screen.blit(font.render('/',True, (255,255,255)), (width*11//48 , height*3//4))
    screen.blit(font.render(str(person1.max_blood),True, (255,255,255)), (width*7//24 , height*3//4))
    screen.blit(font.render(str(person2.blood),True, (255,255,255)), (width*2//3 , height*3//4))
    screen.blit(font.render('/',True, (255,255,255)), (width*35//48 , height*3//4))
    screen.blit(font.render(str(person2.max_blood),True, (255,255,255)), (width*19//24 , height*3//4))
    
    #print('blood2:',person2.blood)
    #print('_________________')
    pygame.display.flip()
    
def fight(screen, person1, person2, tag):
    bg = (0,0,0)
    height = screen.get_height()
    width = screen.get_width()
    
    face1 = pygame.transform.scale(person1.face, \
                                   (width//4, height//4))
    face2 = pygame.transform.scale(person2.face, \
                                   (width//4, height//4))
    

    refresh(screen, person1, person2, face1, face2)
    
    pygame.time.delay(1000)
    tag1 = True
    tag2 = True

    if person1.equip.type == '剑':
        defence2 = person2.defence
        if person2.equip != None:
            if person2.equip.type == '枪':
                damage1 = person1.strength + person1.equip.damage - 1
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage + 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '斧':
                damage1 = person1.strength + person1.equip.damage + 1
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage - 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type in ('弓','剑'):
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            else:
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
        else:
            damage1 = person1.strength + person1.equip.damage
            hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                
    elif person1.equip.type == '枪':
        defence2 = person2.defence
        if person2.equip != None:
            if person2.equip.type == '斧':
                damage1 = person1.strength + person1.equip.damage - 1
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage + 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '剑':
                damage1 = person1.strength + person1.equip.damage + 1
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage - 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type in ('弓','枪'):
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            else:
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
        else:
            damage1 = person1.strength + person1.equip.damage
            hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                
    elif person1.equip.type == '斧':
        
        defence2 = person2.defence
        if person2.equip != None:
            if person2.equip.type == '剑':
                damage1 = person1.strength + person1.equip.damage - 1
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage + 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '枪':
                damage1 = person1.strength + person1.equip.damage + 1
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage - 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type in ('弓','斧'):
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            else:
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
        else:
            damage1 = person1.strength + person1.equip.damage
            hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                
    elif person1.equip.type == '弓':
        defence2 = person2.defence
        if person2.equip != None:
            if person2.equip.type in ('弓', '剑', '枪', '斧'):
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            else:
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
        else:
            damage1 = person1.strength + person1.equip.damage
            hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit

    elif person1.equip.type == '光':
        defence2 = person2.magic_defence
        if person2.equip != None:
            if person2.equip.type == '理':
                damage1 = person1.strength + person1.equip.damage - 1
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage + 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '暗':
                damage1 = person1.strength + person1.equip.damage + 1
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage - 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '光':
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            else:
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
        else:
            damage1 = person1.strength + person1.equip.damage
            hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                
    elif person1.equip.type == '理':
        defence2 = person2.magic_defence
        if person2.equip != None:
            if person2.equip.type == '暗':
                damage1 = person1.strength + person1.equip.damage - 1
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage + 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '光':
                damage1 = person1.strength + person1.equip.damage + 1
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage - 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '光':
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            else:
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
        else:
            damage1 = person1.strength + person1.equip.damage
            hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit

    elif person1.equip.type == '暗':
        defence2 = person2.magic_defence
        if person2.equip != None:
            if person2.equip.type == '光':
                damage1 = person1.strength + person1.equip.damage - 1
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage + 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '理':
                damage1 = person1.strength + person1.equip.damage + 1
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage - 1
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            elif person2.equip.type == '光':
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.magic_defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
            else:
                damage1 = person1.strength + person1.equip.damage
                defence1 = person1.defence
                damage2 = person2.strength + person2.equip.damage
                hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit
                hit2 = (person2.skill - person1.speed)*5 + person2.equip.hit
        else:
            damage1 = person1.strength + person1.equip.damage
            hit1 = (person1.skill - person2.speed)*5 + person1.equip.hit

    

    #首轮攻击
    person1.equip.endure -= 1
    tag1 = person1.check_equip()
    a = random.random()
    if a> hit1/100:
        flag = -1
    else: flag = 0

    if flag != -1 and damage1 > defence2:
        flag = damage1 - defence2
        person2.blood -= flag
        if person2.blood < 0:
                person2.blood = 0
    refresh(screen, person1, person2, face1, face2, hurt2 = flag)
    pygame.time.delay(1000)
    if(person2.blood == 0): return
    
    #反击
    if tag == True:
        person2.equip.endure -= 1
        tag2 = person1.check_equip()
        a = random.random()
        if a> hit2/100:
            flag = -1
        else: flag = 0
        if flag != -1 and damage2 > defence1:
            flag = damage2 - defence1
            person1.blood -= flag
            if person1.blood < 0:
                    person1.blood = 0  
        refresh(screen, person1, person2, face1, face2, hurt1 = flag)
        pygame.time.delay(1000)
        if(person1.blood == 0): return
        
    #追击
    if tag1 and person1.speed > person2.speed + 3:
        person2.equip.endure -= 1
        tag2 = person1.check_equip()
        a = random.random()
        if a> hit1/100:
            flag = -1
        else: flag = 0
        if flag != -1 and damage1 > defence2:
            flag = damage1 - defence2
            person2.blood -= flag
            if person2.blood < 0:
                person2.blood = 0
        refresh(screen, person1, person2, face1, face2, hurt2 = flag)
        pygame.time.delay(1500)
        
    elif tag and tag2 and person1.speed + 3 < person2.speed:
        person2.equip.endure -= 1
        tag2 = person1.check_equip()
        a = random.random()
        if a> hit2/100:
            flag = -1
        else: flag = 0
        if flag != -1 and damage2 > defence1:
            flag = (damage2 - defence1)
            person1.blood -= flag
            if person1.blood < 0:
                person1.blood = 0
        
        refresh(screen, person1, person2, face1, face2, hurt1 = flag)
        pygame.time.delay(1000)

    if tag1 == False:
        person1.to_equip()
    if tag2 == False:
        person2.to_equip()
