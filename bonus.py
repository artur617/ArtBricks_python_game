import random
import pygame

class Bonus():
    def createBonus(self):
        random_int = random.randint(0,300)
        self.mode = "none"

        if random_int >0 and random_int <10:
            self.bonus3balls()
        if random_int >11 and random_int <18:
            self.bonus5balls()
        if random_int >19 and random_int <24:
            self.bonus7balls()
        if random_int >25 and random_int <30:
            self.catchBall()
        if random_int >31 and random_int <35:
            self.superBall()

    def makeBonus(self, thisForm):
       if self.mode == '3balls':
          self.bonus_3baals(thisForm)
       if self.mode == '5balls':
          self.bonus_5baals(thisForm)
       if self.mode == '7balls':
          self.bonus_7baals(thisForm)
       if self.mode == 'catchBall':
          self.bonus_catchBall(thisForm)
       if self.mode == 'superBall':
          self.bonus_superBall(thisForm)

    def bonus3balls(self):
        self.bonus_img = pygame.image.load("data/3balls.png").convert_alpha()
        self.rect = self.bonus_img.get_rect()
        self.bricklength = self.rect.right - self.rect.left
        self.brickheight = self.rect.bottom - self.rect.top
        self.xpos = self.xpos+8
        self.mode = "3balls"

    def bonus5balls(self):
        self.bonus_img = pygame.image.load("data/5balls.png").convert_alpha()
        self.rect = self.bonus_img.get_rect()
        self.bricklength = self.rect.right - self.rect.left
        self.brickheight = self.rect.bottom - self.rect.top
        self.xpos = self.xpos+4
        self.mode = "5balls"

    def bonus7balls(self):
        self.bonus_img = pygame.image.load("data/7balls.png").convert_alpha()
        self.rect = self.bonus_img.get_rect()
        self.bricklength = self.rect.right - self.rect.left
        self.brickheight = self.rect.bottom - self.rect.top
        self.xpos = self.xpos+0
        self.mode = "7balls"

    def catchBall(self):
        self.bonus_img = pygame.image.load("data/catch_ball.png").convert_alpha()
        self.rect = self.bonus_img.get_rect()
        self.bricklength = self.rect.right - self.rect.left
        self.brickheight = self.rect.bottom - self.rect.top
        self.xpos = self.xpos+8

        self.mode = "catchBall"

    def superBall(self):
        self.bonus_img = pygame.image.load("data/mario_fireball_special.gif").convert_alpha()
        self.rect = self.bonus_img.get_rect()
        self.bricklength = self.rect.right - self.rect.left
        self.brickheight = self.rect.bottom - self.rect.top
        self.xpos = self.xpos+12

        self.mode = "superBall"
    
        
    def bonus_3baals(self,thisForm):
        for i in range(3):
            thisForm.balls_array.append(thisForm.ball(thisForm))
            thisForm.balls_array[len(thisForm.balls_array)-1].visible = 1
            thisForm.balls_array[len(thisForm.balls_array)-1].go = 1

    def bonus_5baals(self,thisForm):
        for i in range(5):
            thisForm.balls_array.append(thisForm.ball(thisForm))
            thisForm.balls_array[len(thisForm.balls_array)-1].visible = 1
            thisForm.balls_array[len(thisForm.balls_array)-1].go = 1
    def bonus_7baals(self,thisForm):
        for i in range(7):
            thisForm.balls_array.append(thisForm.ball(thisForm))
            thisForm.balls_array[len(thisForm.balls_array)-1].visible = 1
            thisForm.balls_array[len(thisForm.balls_array)-1].go = 1
    def bonus_catchBall(self,thisForm):
        thisForm.ball_catch_bonus = 1
        thisForm.bonus_good_time = random.randint(1,20)*60
        #thisForm.bonus_mad_time = 600#thisForm.bonus_mad_time + random.randint(100,2000)
        
    def bonus_superBall(self,thisForm):
        for ball in thisForm.balls_array:
            ball.superBall = 1
        thisForm.bonus_good_time = random.randint(1,7)*60
        #thisForm.bonus_mad_time = 600#thisForm.bonus_mad_time + random.randint(100,2000)
   

    def __init__(self, xpos, ypos, level):
        self.xpos = xpos
        self.ypos = ypos
        self.level = level
        self.destruct = 0
        self.createBonus()
        self.speed = random.randint(3,10)
        
    def show(self, thisForm):
            if self.mode != "none":
                self.ypos = self.ypos+self.speed
                thisForm.screen.blit(self.bonus_img, (self.xpos, self.ypos))
            
    def getRect(self):
        return self.bonus_img.get_rect()

    def action(self, thisForm):
        if self.mode != "none":
          rect = self.getRect()

          mouse_pos = pygame.mouse.get_pos()
          #print self.rect.top

          if mouse_pos[1] < 400:
              paddle_y_pos = 400
          else:
              paddle_y_pos = mouse_pos[1]
            #zlapanie bonusa paletka

          if self.xpos > mouse_pos[0]-16-43 and self.xpos < mouse_pos[0]+84+18-43 and self.ypos < paddle_y_pos+30-12 and self.ypos > paddle_y_pos-15:
              self.destruct = 1
              self.makeBonus(thisForm)
          if thisForm.height < self.ypos:
              self.destruct = 1