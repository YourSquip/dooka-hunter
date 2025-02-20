from typing import Any
import pygame
import math
from sys import exit
from random import randint
import time

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('dooka hunter')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts/Lovely Valentine.otf', 50)
test_font_small = pygame.font.Font('fonts/Lovely Valentine.otf', 20)
test_font_big = pygame.font.Font('fonts/Lovely Valentine.otf', 100)
pygame.mouse.set_visible(False)

new_icon = pygame.image.load('sprites/dooka_icon.png')
pygame.display.set_icon(new_icon)


def text_message(message):
    text_box = pygame.image.load('sprites/text_box.png')
    screen.blit(text_box,(0,0))
    text_area = test_font.render(message,False, 'Crimson')
    text_rect = text_area.get_rect(topleft = (200,600))
    screen.blit(text_area,text_rect)  

def draw_words():
    if(mirror_group.sprite.with_words):
                    screen.blit(mirror_group.sprite.words,(0,0))
   
def endless_sprites(srf,rect1,rect2,rect3):
        screen.blit(srf,rect1)
        screen.blit(srf,rect2)
        screen.blit(srf,rect3)
        rect1.left -= 2
        rect2.left -=2
        rect3.left -=2
        if rect1.right <= 0: rect1.left = rect3.right
        if rect2.right <= 0: rect2.left = rect1.right
        if rect3.right <= 0: rect3.left = rect2.right

def collision_sprite():
        if pygame.sprite.spritecollide(player,obstacle_group,False, pygame.sprite.collide_mask):
            return "game_over"
        else: return "runner"

def draw_game_over_screen():
    screen.fill((0, 0, 0))
    title = test_font_big.render('GAME OVER', True, 'Crimson')
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/2))
    title2 = test_font.render('come on! do it for love!', True, 'Crimson')
    screen.blit(title2, (screen_width/2 - title2.get_width()/2, screen_height/2 - title2.get_height()/2+100))
    title1 = test_font_small.render('press [X] to try again', True, 'Crimson')
    screen.blit(title1, (screen_width/2 - title.get_width()/2 + 70, screen_height/2 - title.get_height()/2 + 210))

def draw_cutscene(scene,index):
     screen.blit(scene_bgnd,(0,0))
     for i in range(0,index):
        screen.blit(scene[i],(0,0))
     if index <= 3:
            screen.blit(press_space,(0,0))
     


class Candle(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()

         #self.image = pygame.image.load('sprites/candle.png').convert_alpha()
         self.sprite_lit = pygame.image.load('sprites/candle_lit.png').convert_alpha()
         self.sprite_base = pygame.image.load('sprites/candle.png').convert_alpha()
         self.sprite_light = pygame.image.load('sprites/camdle_light1.png').convert_alpha()
         self.sprite_light1 =  pygame.image.load('sprites/candle_light2.png').convert_alpha()
         self.sprite_light_lit = pygame.image.load('sprites/candle_light_lit.png').convert_alpha()
         self.lighted = False
         self.anim_index = 0
         self.candle_burn = [self.sprite_light,self.sprite_light1]
         self.image = self.candle_burn[self.anim_index]
         self.rect = self.image.get_rect()
         self.mask = pygame.mask.from_surface(self.image)
    def animation_state(self):
        if self.lighted:
            self.anim_index += 0.1
            if self.anim_index >= len(self.candle_burn): self.anim_index = 0
            self.image = self.candle_burn[int(self.anim_index)]
   
    def update(self,lit):
        if self.lighted == False:
            if lit:
                self.image = self.sprite_lit
            else:
                self.image = self.sprite_base
        else:
            if lit:
                self.image = self.sprite_light_lit
            else:
                #self.image = self.sprite_light
                 self.animation_state()
        
    def light(self): 
        self.lighted = True

class Matchbox(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         self.image = pygame.image.load('sprites/matchbox.png').convert_alpha()
         self.rect = self.image.get_rect()
         self.mask = pygame.mask.from_surface(self.image)
         self.sprite_lit = pygame.image.load('sprites/matchbox_lit.png').convert_alpha()
         self.sprite_base = pygame.image.load('sprites/matchbox.png').convert_alpha()
    def update(self,lit):
        if lit:
            self.image = self.sprite_lit
        else:
            self.image = self.sprite_base

class Book(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         self.image = pygame.image.load('sprites/book.png').convert_alpha()
         self.rect = self.image.get_rect()
         self.mask = pygame.mask.from_surface(self.image)
         self.sprite_lit = pygame.image.load('sprites/book_lit.png').convert_alpha()
         self.sprite_base = pygame.image.load('sprites/book.png').convert_alpha()
    def update(self,lit):
        if lit:
            self.image = self.sprite_lit
        else:
            self.image = self.sprite_base

class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, text1):
            self.image = pygame.image.load('sprites/text_box.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.sprite_empty = pygame.image.load('sprites/empty.png').convert_alpha()
            self.sprite_box = pygame.image.load('sprites/text_box.png').convert_alpha()
            self.font = test_font
            self.size = 16
            self.text = text
            self.text1 = text1
            self.antialias = True
            self.color = 'crimson'
            self.background = None
            self.dialogue = False
            
            self.text = self.font.render(self.text, self.antialias, self.color, self.background)
            self.text1 = self.font.render(self.text1, self.antialias, self.color, self.background)
    def textblit(self):
         if self.dialogue:
             screen.blit(self.image,self.rect)
             screen.blit(self.text, (200,580))
             screen.blit(self.text1, (200,620))
 
   

class Lipstick(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         self.image = pygame.image.load('sprites/lipstick.png').convert_alpha()
         self.rect = self.image.get_rect()
         self.mask = pygame.mask.from_surface(self.image)
         self.sprite_lit = pygame.image.load('sprites/lipstick_lit.png').convert_alpha()
         self.sprite_base = pygame.image.load('sprites/lipstick.png').convert_alpha()
         self.took = False
    def update(self,lit):
        if self.took:
            self.image = pygame.image.load('sprites/empty.png').convert_alpha()
        else:
            if lit:
                self.image = self.sprite_lit
            else:
                self.image = self.sprite_base
        

class Mirror(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         
         self.sprite_lit = pygame.image.load('sprites/mirror_lit.png').convert_alpha()
         self.sprite_base = pygame.image.load('sprites/mirror.png').convert_alpha()
         self.with_words = False
         self.words = pygame.image.load('sprites/dooka.png').convert_alpha()
         self.sprite_blink = pygame.image.load('sprites/mirror_blink.png').convert_alpha()
         self.anim_index = 0
         self.greg_blink = [self.sprite_base,self.sprite_base,self.sprite_blink, self.sprite_base,self.sprite_base]
         self.image = self.greg_blink[self.anim_index]
         self.rect = self.image.get_rect()
         self.mask = pygame.mask.from_surface(self.image)
    def update(self,lit):
        
        if lit:
            self.image = self.sprite_lit
        else:
            self.animation_state()
        
        if self.with_words:
            screen.blit(self.words,(0,0))
    def draw_on(self):
        self.with_words = True
    def animation_state(self):
        self.anim_index += 0.05
        if self.anim_index >= len(self.greg_blink): 
          self.anim_index = 0
        self.image = self.greg_blink[int(self.anim_index)]
   

class Hand(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()

         self.image = pygame.image.load('sprites/hand.png').convert_alpha()
         self.rect = self.image.get_rect()
         self.mask = pygame.mask.from_surface(self.image)
         self.item_type = "hand"
         self.sprite_hand = pygame.image.load('sprites/hand.png').convert_alpha()
         self.sprite_match = pygame.image.load('sprites/match_light.png').convert_alpha()
         self.sprite_lipstick = pygame.image.load('sprites/lipstick_eq.png').convert_alpha()
         self.trials = 0
         self.steps = ""
    def update(self):
        self.rect.center = (pos)
    def hand_on_object(self, group):
        if pygame.sprite.spritecollide(self,group, False,pygame.sprite.collide_mask):
            return True
        else: return False
    def take_match(self,matchbox): 
        if matchbox.image == matchbox.sprite_lit:
           self.image = self.sprite_match
           self.item_type = "match"
    def take_lipstick(self,lipstick): 
        if lipstick.image == lipstick.sprite_lit:
           self.image = self.sprite_lipstick
           self.item_type = "lipstick"
           lipstick.took = True
    def drop_object(self):
        if(self.item_type == "lipstick"):
            lipstick.took = False
        self.image = self.sprite_hand
        self.item_type = "hand"
    def light_candle(self,candle_group):
        if self.hand_on_object(candle_group):
            if self.item_type == "match":
                candle_group.sprite.light()
                match_sound.play()
                if('c' not in self.steps):
                    self.trials = self.trials + 1
                    self.steps = self.steps + 'c'
    def draw_on_mirror(self,mirror_group):
        if self.hand_on_object(mirror_group):
            if self.item_type == "lipstick":
                mirror_group.sprite.draw_on()
                if('m' not in self.steps):
                    self.trials = self.trials + 1
                    self.steps = self.steps + 'm'

    def read_the_spell(self,book_group):
        if self.hand_on_object(book_group):
            ritual_words.dialogue = True
            if('b' not in self.steps):
                    self.trials = self.trials + 1
                    self.steps = self.steps + 'b'

            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1  = pygame.image.load('sprites/greg_runs_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('sprites/greg_runs_15.png').convert_alpha()
        player_walk_3 = pygame.image.load('sprites/greg_runs_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2,player_walk_3]
        self.player_index = 0
        self.player_jump = pygame.image.load('sprites/greg_jumps.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(topleft= (0,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.gravity = 0

        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 720:
            self.gravity = -25
            self.mask = pygame.mask.from_surface(self.player_jump)
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 720:
            self.rect.bottom = 720
        
    def animation_state(self):
        if self.rect.bottom < 600:
            self.image = self.player_jump
            
        else:
            self.player_index += 0.1 
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def move_right(self):
         self.rect.x =  self.rect.x + 5
         if self.rect.x > 1200 :self.rect.x = 0
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x_pos):
        super().__init__()

        self.animation_index = 0
        self.image = pygame.image.load('sprites/smaller_box.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_pos,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
    def update(self):
        self.rect.x -= 10
        self.destroy()
    def destroy(self):
        if self.rect.x <= -1000:
            self.kill()


mirror_level_theme = pygame.mixer.Sound('audio/Spook3.mp3')
match_sound = pygame.mixer.Sound('audio/match_sound.mp3')
runner_theme = pygame.mixer.Sound('audio/PerituneMaterial_EpicBattle_J.mp3')

start_theme = pygame.mixer.Sound('audio/library.mp3')
middle_theme = pygame.mixer.Sound('audio/middle.mp3')
ending_theme = pygame.mixer.Sound('audio/ending.mp3')

#CREATING OBJECTS
hand = Hand()

candle = Candle()
matchbox = Matchbox()
lipstick = Lipstick()
mirror = Mirror()
book = Book()

player = Player()



#GROUPS
candle_group = pygame.sprite.GroupSingle()
matchbox_group = pygame.sprite.GroupSingle()
lipstick_group = pygame.sprite.GroupSingle()
mirror_group = pygame.sprite.GroupSingle()
book_group = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()

equipped_group = pygame.sprite.GroupSingle()

player_group = pygame.sprite.GroupSingle()


candle_group.add(candle)
matchbox_group.add(matchbox)
lipstick_group.add(lipstick)
mirror_group.add(mirror)
book_group.add(book)

equipped_group.add(hand)

player_group.add(player)

#TESTING_DRAWING
bgnd_srf = pygame.image.load('sprites/background.png').convert_alpha()
shadow_srf = pygame.image.load('sprites/shadow.png').convert_alpha()

ground_srf = pygame.image.load('sprites/runner_bgnd.png').convert_alpha()
ground1_rect = ground_srf.get_rect(topleft = (0,0))
ground2_rect = ground_srf.get_rect(topleft = (1280,0))
ground3_rect = ground_srf.get_rect(topleft = (2560,0))


fire_back_srf = pygame.image.load('sprites/fire_back_1.png').convert_alpha()
fire_back_srf1 = pygame.image.load('sprites/fire_back_1.png').convert_alpha()
fire_back_srf2 = pygame.image.load('sprites/fire_back_2.png').convert_alpha()
fire_back_anim = [fire_back_srf1,fire_back_srf2]
fire_back_anim_index = 0
fire_back1_rect = fire_back_srf.get_rect(topleft = (0,0))
fire_back2_rect = fire_back_srf.get_rect(topleft = (1280,0))
fire_back3_rect = fire_back_srf.get_rect(topleft = (2560,0))

fire_back1_door = pygame.image.load('sprites/back_fire_door.png').convert_alpha()
fire_back2_door = pygame.image.load('sprites/back_fire_door1.png').convert_alpha()
fire_back_door = pygame.image.load('sprites/back_fire_door.png').convert_alpha()
fire_back_door_anim = [fire_back1_door,fire_back2_door]
fire_back_door_index = 0


fire_front_srf = pygame.image.load('sprites/fire_front_1.png').convert_alpha()
fire_front_srf1 = pygame.image.load('sprites/fire_front_1.png').convert_alpha()
fire_front_srf2 = pygame.image.load('sprites/fire_front_2.png').convert_alpha()
fire_front_anim = [fire_front_srf1,fire_front_srf2]
fire_front_anim_index = 0
fire_front1_rect = fire_front_srf.get_rect(topleft = (0,0))
fire_front2_rect = fire_front_srf.get_rect(topleft = (1280,0))
fire_front3_rect = fire_front_srf.get_rect(topleft = (2560,0))

smoke_srf = pygame.image.load('sprites/smoke1.png').convert_alpha()
smoke_srf1 = pygame.image.load('sprites/smoke1.png').convert_alpha()
smoke_srf2 = pygame.image.load('sprites/smoke2.png').convert_alpha()
smoke_anim = [smoke_srf1,smoke_srf2]
smoke_anim_index = 0
smoke_rect = smoke_srf.get_rect(topleft = (0,0))

scene_bgnd = pygame.image.load('sprites/cutscene1/cutscene1_1.png').convert_alpha()
great_company = pygame.image.load('sprites/fashion_lobsters.png').convert_alpha()
title = pygame.image.load('sprites/title.png').convert_alpha()
scene1_1 = pygame.image.load('sprites/cutscene1/cutscene1_2.png').convert_alpha()
scene1_2 = pygame.image.load('sprites/cutscene1/cutscene1_3.png').convert_alpha()
scene1_3 = pygame.image.load('sprites/cutscene1/cutscene1_4.png').convert_alpha()
scene1_4 = pygame.image.load('sprites/cutscene1/cutscene1_5.png').convert_alpha()
scene1_5 = pygame.image.load('sprites/cutscene1/cutscene1_6.png').convert_alpha()
scene1_6 = pygame.image.load('sprites/cutscene1/cutscene1_7.png').convert_alpha()
scene1 =[great_company,title,scene_bgnd,scene1_1,scene1_2,scene1_3,scene1_4,scene1_5,scene1_6]
scene1_index = 1


scene2_1 = pygame.image.load('sprites/cutscene2/2cutscene1.png').convert_alpha()
scene2_2 = pygame.image.load('sprites/cutscene2/2cutscene2.png').convert_alpha()
scene2_3 = pygame.image.load('sprites/cutscene2/2cutscene3.png').convert_alpha()
scene2_4 = pygame.image.load('sprites/cutscene2/2cutscene4.png').convert_alpha()
scene2_5 = pygame.image.load('sprites/cutscene2/2cutscene5.png').convert_alpha()
scene2_6 = pygame.image.load('sprites/cutscene2/2cutscene6.png').convert_alpha()
scene2_7 = pygame.image.load('sprites/cutscene2/2cutscene7.png').convert_alpha()
scene2_8 = pygame.image.load('sprites/cutscene2/2cutscene8.png').convert_alpha()
scene2_9 = pygame.image.load('sprites/cutscene2/2cutscene9.png').convert_alpha()
scene2_10 = pygame.image.load('sprites/cutscene2/2cutscene10.png').convert_alpha()
scene2 =[scene2_1,scene2_2,scene2_3,scene2_4,scene2_5,scene2_6, scene2_7, scene2_8,scene2_9,scene2_10]
scene2_index = 1


scene3_1 = pygame.image.load('sprites/cutscene3/3cutscene1.png').convert_alpha()
scene3_2 = pygame.image.load('sprites/cutscene3/3cutscene2.png').convert_alpha()
scene3_3 = pygame.image.load('sprites/cutscene3/3cutscene3.png').convert_alpha()
scene3_4 = pygame.image.load('sprites/cutscene3/3cutscene4.png').convert_alpha()
scene3_5 = pygame.image.load('sprites/cutscene3/3cutscene5.png').convert_alpha()
scene3_6 = pygame.image.load('sprites/cutscene3/3cutscene6.png').convert_alpha()
scene3_7 = pygame.image.load('sprites/cutscene3/3cutscene7.png').convert_alpha()
ending_art = pygame.image.load('sprites/ending_art.png').convert_alpha()
credits = pygame.image.load('sprites/credits_new.png').convert_alpha()

scene3 =[scene3_1,scene3_2,scene3_3,scene3_4,scene3_5,scene3_6, scene3_7, ending_art, credits]
scene3_index = 1

press_space = pygame.image.load('sprites/space1.png').convert_alpha()
tutor_page = pygame.image.load('sprites/press1.png').convert_alpha()



door_srf = pygame.image.load('sprites/door.png').convert_alpha()

back_fire_animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(back_fire_animation_timer,500)

front_fire_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(front_fire_animation_timer,500)

box_spawn_timer = pygame.USEREVENT + 3
pygame.time.set_timer(box_spawn_timer,2500)

smoke_animation_timer =  pygame.USEREVENT + 4
pygame.time.set_timer(smoke_animation_timer,600)

fire_back_door_animation_timer =  pygame.USEREVENT + 5
pygame.time.set_timer(fire_back_door_animation_timer,500)

#PHARSES
ritual_words= TextBox('dooka,dooka,dooka!','')
wrong_order = TextBox('huh...I think I messed up with the order','okay, let\'s try this again...')
did_it = TextBox('that should do it i guess','')

wrong_comb = False
correct_order = False
level = "start_cutscene"
cutscene = True

obstacles_cnt = 0
end_of_room = False
prev = 0
tutor_jump = True
start_theme.play()
start_theme.set_volume(0.5)

while True:

    if level == 'start_cutscene':
        if(scene1_index<=len(scene1)):
             draw_cutscene(scene1,scene1_index)
    if level == 'mirror_level':
                
                cutscene = False
                if(hand.steps != "cmb" and hand.trials>=3):
                    wrong_order.dialogue = True
                    hand.trials = 0
                    hand.steps = ""
                    hand.item_type = "hand"
                    hand.image = hand.sprite_hand
                    lipstick.took = False
                    mirror.with_words = False
                    candle.lighted = False
                    candle.image = candle.sprite_base
                elif(hand.steps == "cmb" and  hand.trials==3):
                     correct_order = True
                     middle_theme.play()
                
                    
                pos = pygame.mouse.get_pos()

                matchbox_lit = hand.hand_on_object(matchbox_group)
                lipstick_lit = hand.hand_on_object(lipstick_group)
                candle_lit =  hand.hand_on_object(candle_group)
                mirror_lit = hand.hand_on_object(mirror_group)
                book_lit = hand.hand_on_object(book_group)
   
                screen.blit(bgnd_srf,(0,0))
                screen.blit(tutor_page,(0,0))
     

                mirror_group.update(mirror_lit)
                lipstick_group.update(lipstick_lit)
                candle_group.update(candle_lit)
                matchbox_group.update(matchbox_lit)
                book_group.update(book_lit)
   
                equipped_group.update()
    
                mirror_group.draw(screen)
                matchbox_group.draw(screen)
                lipstick_group.draw(screen)
                candle_group.draw(screen)
                book_group.draw(screen)

                draw_words()
                screen.blit(shadow_srf,(0,0))

        #TEXT
                ritual_words.textblit()
                wrong_order.textblit()
                did_it.textblit()
        
       

                equipped_group.draw(screen)
    #HANDLING EVENTS
    if level == 'gotta_run':
                if(scene2_index<=len(scene2)):
                    draw_cutscene(scene2,scene2_index)
                
    if level == 'runner':
                
                if not end_of_room:
                    endless_sprites(ground_srf,ground1_rect,ground2_rect,ground3_rect)
                    endless_sprites(fire_back_srf,fire_back1_rect,fire_back2_rect,fire_back3_rect)
                    player_group.draw(screen)
                    player_group.update()
                    obstacle_group.draw(screen)
                    obstacle_group.update()
                    endless_sprites(fire_front_srf,fire_front1_rect,fire_front2_rect,fire_front3_rect)
                    if tutor_jump:
                         screen.blit(press_space,(0,0))
                    level = collision_sprite()
                else:
                    
                    screen.blit(door_srf,(0,0))
                    screen.blit(fire_back_door,(0,0))
                    player.move_right()
                    player_group.draw(screen)
                    player_group.update()
                    screen.blit(fire_front_srf,(0,0))
                    if player.rect.x > 900:
                         level = "ending"
                         runner_theme.stop()
                         ending_theme.play()
                screen.blit(smoke_srf,(0,0))
                     

    if level == 'ending':
                if(scene3_index<=len(scene3)):
                    draw_cutscene(scene3,scene3_index)
    if level == 'game_over':
                draw_game_over_screen()
                runner_theme.stop()
            
    for event in pygame.event.get():
           
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        ritual_words.dialogue = False
                        wrong_order.dialogue = False

                        hand.take_match(matchbox)
                        hand.take_lipstick(lipstick)
                        hand.light_candle(candle_group)
                        hand.draw_on_mirror(mirror_group)
                        hand.read_the_spell(book_group)
                        if level == "mirror_level" and correct_order:
                             mirror_level_theme.stop()
                             level = "gotta_run"
                            
                    if event.button == 3:
                        hand.drop_object()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ritual_words.dialogue = False
                        wrong_order.dialogue = False

                        if level == "mirror_level" and correct_order:  
                             mirror_level_theme.stop()
                             middle_theme.play()
                             level = "gotta_run"
                             
                        if level == "start_cutscene":
                             scene1_index= scene1_index+1
                             if(scene1_index > len(scene1)):
                                  level = "mirror_level"
                                  start_theme.stop()
                                  mirror_level_theme.play()
                                  mirror_level_theme.set_volume(0.2)
                        if level == "runner":
                             tutor_jump = False
                        if level == "gotta_run":
                             scene2_index= scene2_index+1
                             if(scene2_index > len(scene2)):
                                  level = "runner"
                                  middle_theme.stop()
                                  runner_theme.play()
                                  runner_theme.set_volume(0.6)
                                  

                        if level == "ending":
                             scene3_index= scene3_index+1
                             if(scene3_index > len(scene3)):
                                  pygame.quit()
                                  exit()
                    if event.key == pygame.K_x:
                         if level  =="game_over":
                              obstacle_group.empty()
                              obstacles_cnt = 0
                              level = "runner"
                              runner_theme.play()

                if level == 'runner':
                    if event.type == back_fire_animation_timer:
                        if fire_back_anim_index ==0: fire_back_anim_index = 1
                        else: fire_back_anim_index = 0
                        fire_back_srf = fire_back_anim[fire_back_anim_index]
                    if event.type == front_fire_animation_timer:
                        if fire_front_anim_index ==0: fire_front_anim_index = 1
                        else: fire_front_anim_index = 0
                        fire_front_srf = fire_front_anim[fire_front_anim_index]
                    if event.type == box_spawn_timer:
                         if not end_of_room:
                            obst_pos = randint(600,1500)
                            if(obst_pos-prev < 500):
                                 obst_pos = obst_pos + 200
                            elif(prev - obst_pos < 500):
                                 obst_pos = obst_pos - 200
                            prev = obst_pos
                            obstacle_group.add(Obstacle(obst_pos))
                            obstacles_cnt = obstacles_cnt + 1
                            if obstacles_cnt >= 10:
                                end_of_room = True
                    if event.type == smoke_animation_timer:
                        if smoke_anim_index ==0: smoke_anim_index = 1
                        else: smoke_anim_index = 0
                        smoke_srf = smoke_anim[smoke_anim_index]
                    if event.type == fire_back_door_animation_timer:
                        if fire_back_door_index ==0: fire_back_door_index = 1
                        else: fire_back_door_index = 0
                        fire_back_door = fire_back_door_anim[fire_back_door_index]
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    pygame.display.update()
    clock.tick(60)
    
