# -*- coding: utf-8 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.


import pygame
from pydoc import visiblename
import random
import brick
import sys
import bonus
from pygame.locals import * #need this for 'FULLSCREEN' value
import os
import levels


from win32api import GetSystemMetrics
os.environ['SDL_VIDEO_WINDOW_POS'] = str((GetSystemMetrics (0)/2)-512) + "," + str((GetSystemMetrics (1)/2)-384)

class game():
    class ball():
        visible = 0;
        
        def __init__(self, thisForm):
            start_direction = random.randint(-10, 10)
            self.speed=[start_direction,8]
            self.superBall = 0;
            self.ball=pygame.image.load("data/white-ball.png")
            #self.paddle_pong = pygame.mixer.Sound('data/paddle_pong.wav')
            self.ballAction=self.ball.get_rect()
            #self.ballAction.left = (random.randint(0, thisForm.width))
            #self.ballAction.top = (random.randint(0, 200))
            self.go = 0
            self.odrzut = 46
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] < 458:
                    paddle_y_pos = 458
            else:
                    paddle_y_pos = mouse_pos[1]
                    
            self.ballAction.left = mouse_pos[0]+self.ballAction.bottom-self.ballAction.top+10-43
            self.ballAction.top = paddle_y_pos+self.ballAction.left-self.ballAction.right-12

        def action(self, thisForm):
            mouse_pos = pygame.mouse.get_pos()

            if self.superBall == 1:
                self.ball=pygame.image.load("data/superball.gif")
            else:
                self.ball=pygame.image.load("data/white-ball.png")
            if mouse_pos[1] < 458:
                    paddle_y_pos = 458
            else:
                    paddle_y_pos = mouse_pos[1]
            if self.visible == 1:
            
              
              if self.go != 0:
                self.ballAction = self.ballAction.move(self.speed)
              else:
                self.ballAction.left = mouse_pos[0]+self.ballAction.bottom-self.ballAction.top+10-43+self.odrzut-46
                self.ballAction.top = paddle_y_pos+self.ballAction.left-self.ballAction.right-12


            # Uderzenie w sciany
              if self.ballAction.left < 0 or self.ballAction.right > thisForm.width:
                    self.speed[0] = -self.speed[0]
              if self.ballAction.top <= 24:
                    self.speed[1] = -self.speed[1]
              if self.ballAction.top > thisForm.height:
                  self.visible = 0
                  print "koniec"
                  self.speed[1] = -self.speed[1]

              
              #zderzenie z paletka
              if self.ballAction.left > mouse_pos[0]-16-43 and self.ballAction.right < mouse_pos[0]+84+18-43 and self.ballAction.bottom < paddle_y_pos+30-12 and self.ballAction.bottom > paddle_y_pos-15:
                  if self.speed[1] > 0:
                    self.speed[1] = -self.speed[1]
                    #self.paddle_pong.play(0)
                  self.odrzut = self.ballAction.left - mouse_pos[0]+16+43
                  # (-5 + _100_/10)(-5,+5)   (-10 + _100/5)(-10, +10)
                  #self.speed[0] = self.speed[0] +(-5 + odrzut/10) + random.randint(-1, 1)
                  self.speed[0] = (-10 + self.odrzut/5) + random.randint(-1, 1)
                  if thisForm.ball_catch_bonus == 1:
                    self.go = 0
                  if self.visible == 0:
                    del self
        def show(self, thisForm):
            if self.visible == 1:
                thisForm.screen.blit(self.ball, self.ballAction)

    def clearBalls(self):
        for ball in self.balls_array:
                ball.visible = 0
        for ball in range(0, 1, 1):
            self.balls_array.append(self.ball(self))
        self.balls_array[0].visible = 1;
        self.balls_array[0].go = 0;
    def load_sliced_sprites(self, w, h, filename):
        '''
        Specs :
            Master can be any height.
            Sprites frames width must be the same width
            Master width must be len(frames)*frame.width
        Assuming you ressources directory is named "ressources"
        '''
        images = []
        master_image = pygame.image.load(filename).convert_alpha()

        master_width, master_height = master_image.get_size()
        for i in xrange(int(master_width/w)):
            images.append(master_image.subsurface((i*w,0,w,h)))
        return images

    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.

        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t

    def newLevel(self):
       self.current_lvl += 1
       self.clearBalls()

    def __init__(self):
        # zapobiega w opuznieniach miedzy zbiciem a dzwiekiem
        # pobrane dzwieki z http://www.pacdv.com/sounds/interface_sounds-2.html
        
        #self.background = pygame.image.load('data/back1.jpg')
        #pygame.mixer.pre_init(frequency=22050, size=-16, channels=8, buffer=256)

        self.fullscreen = 0
        self.start_main = 1
        pygame.init()
        
        size=self.width, self.height=1024, 768

        if self.fullscreen == 1:
            self.screen = pygame.display.set_mode((size),FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((size))

        self.background = pygame.image.load('data/back1.jpg')
        self.ball_catch_bonus = 0
        
        self.bonus_good_time = 0
        self.bonus_mad_time = 0

        self.lives = 3
        self.points = 0
        self.point_multi = 1

        self.current_lvl = 0

        #self.brick_destroy_wav = pygame.mixer.Sound('data/bang_5.wav')

        #self.brick_destroy_wav.set_volume(1)
        color=147,179,253


        
        dog=pygame.image.load("data/pies.gif")
        
        font = pygame.font.Font(None, 16)
        self.font_brick = pygame.font.Font(None, 15)
        font_start = pygame.font.Font(None, 23)
        odrzut = 0
        #pygame.mouse.set_visible(False)

        diamond = ((16, 16), (7, 7),
            (0, 0, 1, 0, 3, 128, 7, 192, 14, 224, 28, 112, 56, 56, 112, 28, 56,
             56, 28, 112, 14, 224, 7, 192, 3, 128, 1, 0, 0, 0, 0, 0),
            (1, 0, 3, 128, 7, 192, 15, 224, 31, 240, 62, 248, 124, 124, 248, 62,
             124, 124, 62, 248, 31, 240, 15, 224, 7, 192, 3, 128, 1, 0, 0, 0))


        broken_x = ((16, 16), (7, 7),
            (0, 0, 96, 6, 112, 14, 56, 28, 28, 56, 12, 48, 0, 0, 0, 0, 0, 0, 0, 0,
             12, 48, 28, 56, 56, 28, 112, 14, 96, 6, 0, 0),
            (224, 7, 240, 15, 248, 31, 124, 62, 62, 124, 30, 120, 14, 112, 0, 0, 0,
             0, 14, 112, 30, 120, 62, 124, 124, 62, 248, 31, 240, 15, 224, 7))

        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        
        pygame.display.flip()
        ik = 0
        step = 1
        clock = pygame.time.Clock()

        self.text2 = font.render('x: ', True, (255,255, 255))
        self.balls_array = []
        self.bonus_array = []
        for ball in range(0, 1, 1):
            self.balls_array.append(self.ball(self))

        self.balls_array[0].visible = 1;

        bricks = brick.Brick("data/green_brick.png")
        logo = pygame.image.load("data/logo.png").convert_alpha()

        """bricks.build_wall_unbreake(self.width)
        bricks.build_wall(self.width)
        bricks.build_wall_fewHit(self.width)"""
        bricks.build_simple_level(levels.level[self.current_lvl], self.width)
        temp = 0
        a = 2

        while True:
           if self.start_main == 1:
              for event in pygame.event.get():
                      if event.type == pygame.QUIT: sys.exit()
              
              if (event.type == KEYUP):
                if (event.key == K_ESCAPE):
                    sys.exit(0)
                if (event.key == K_f):
                    if self.fullscreen == 0:
                        self.fullscreen = 1
                        self.screen = pygame.display.set_mode((size),FULLSCREEN)
                    else:
                        self.fullscreen = 0
                        self.screen = pygame.display.set_mode((size))

              clock.tick(60)
              colorS = 0,0,0
              self.screen.fill(colorS)
              self.screen.blit(logo, (1, 1))
              text = font_start.render("ZADANIE - Zbij wszystkie klocki ", True, (211,222, 233))
              self.screen.blit(text, (100, 400))
              text = font_start.render("KLAWISZE", True, (211,222, 233))
              self.screen.blit(text, (100, 430))
              text = font_start.render("F - fullscreen", True, (211,222, 233))
              self.screen.blit(text, (120, 450))
              text = font_start.render(u"ESC - Wyjście", True, (211,222, 233))
              self.screen.blit(text, (120, 470))
              text = font_start.render("S - Superball", True, (211,222, 233))
              self.screen.blit(text, (120, 490))
              text = font_start.render("N - Nowa kula", True, (211,222, 233))
              self.screen.blit(text, (120, 510))
              text = font_start.render("Lewy przycisk myszy - START", True, (210,11, 11))
              self.screen.blit(text, (420, 540))
              mousebutton = pygame.mouse.get_pressed()

              if mousebutton[0] == 1:
                a = 1
              if mousebutton[0] == 0:
                  if a == 1:
                    self.start_main = 0
              pygame.display.flip()
           else:
              for event in pygame.event.get():
                      if event.type == pygame.QUIT: sys.exit()

              # 60 frames per second
              clock.tick(50)

              if len(bricks.brickrect)+len(bricks.brickrect_fewHit) == 0:
                  self.clearBalls()
                  if len(self.balls_array) <= 3:
                    self.newLevel()
                    self.clearBalls()
                    bricks.build_simple_level(levels.level[self.current_lvl], self.width)

              if len(self.balls_array) < 1:
                  self.clearBalls()
                  self.lives -= 1

              ''' Asuming your frames have a 16x16 size '''
              #explosion_images = self.load_sliced_sprites(20, 20, 'data/explosed-sprite.png')
              paddle = self.load_sliced_sprites(84, 24, 'data/ark.png')


              for ball in self.balls_array:
                  ball.action(self)


              for ind in range(len(self.balls_array)):
                  try:
                      if self.balls_array[ind].visible == 0:
                        del self.balls_array[ind]
                  except :
                      print "e02"



              for ball in self.balls_array:
                  index = ball.ballAction.collidelist(bricks.brickrect)
                    # check if ball has hit wall
                    # if yes yhen delete brick and change ball direction
                  if index != -1:
                        #self.brick_destroy_wav.play(0)
                        if ball.superBall != 1:
                            if ball.ballAction.right-8 > bricks.brickrect[index].right or \
                               ball.ballAction.left+8 < bricks.brickrect[index].left:
                                  if ball.ballAction.right > bricks.brickrect[index].right:
                                        if ball.speed[0] > -3 and ball.speed[0] < 3:
                                            ball.speed[0] = -2
                                            ball.speed[1] = -ball.speed[1]
                                  if ball.ballAction.left < bricks.brickrect[index].left:
                                        if ball.speed[0] > -3 and ball.speed[0] < 3:
                                            ball.speed[0] = 2
                                            ball.speed[1] = -ball.speed[1]

                                  ball.speed[0] = -ball.speed[0]

                            else:
                                if ball.ballAction.top > bricks.brickrect[index].top or \
                                    ball.ballAction.bottom < bricks.brickrect[index].bottom:
                                  if ball.speed[1] < 0:

                                    ball.speed[1] = -ball.speed[1]
                                  else:

                                    ball.speed[1] = -ball.speed[1]

                        self.bonus_array.append(bonus.Bonus(bricks.brickrect[index].left,bricks.brickrect[index].top,1))

                        bricks.brickrect[index:index + 1] = []
                        self.points += 10 * self.point_multi

                  index_unbreake = ball.ballAction.collidelist(bricks.brickrect_unbreake)
                    # check if ball has hit wall
                    # if yes yhen delete brick and change ball direction
                  if index_unbreake != -1:
                        #self.brick_destroy_wav.play(0)
                        if ball.superBall != 1:
                            if ball.ballAction.center[0] > bricks.brickrect_unbreake[index_unbreake].right or \
                               ball.ballAction.center[0] < bricks.brickrect_unbreake[index_unbreake].left:
                                  if ball.ballAction.center[0] > bricks.brickrect_unbreake[index_unbreake].right:
                                        ball.ballAction.left = bricks.brickrect_unbreake[index_unbreake].right
                                        if ball.speed[0] == 0:
                                            ball.speed[0] = -3
                                        ball.speed[0] = -ball.speed[0]
                                  if ball.ballAction.center[0] < bricks.brickrect_unbreake[index_unbreake].left:
                                        ball.ballAction.right = bricks.brickrect_unbreake[index_unbreake].left
                                        if ball.speed[0] == 0:
                                            ball.speed[0] = 3
                                        ball.speed[0] = -ball.speed[0]

                            else:
                                if ball.ballAction.top > bricks.brickrect_unbreake[index_unbreake].top or \
                                    ball.ballAction.bottom < bricks.brickrect_unbreake[index_unbreake].bottom:
                                  self.text2 = font.render('x: ' + str(ball.ballAction.center[0]) + " Y: "+ str(bricks.brickrect_unbreake[index_unbreake].left), True, (255,255, 255))
                                  if ball.speed[1] < 0:
                                    ball.ballAction.top = bricks.brickrect_unbreake[index_unbreake].bottom
                                    ball.speed[1] = -ball.speed[1]
                                  else:
                                    ball.ballAction.bottom = bricks.brickrect_unbreake[index_unbreake].top
                                    ball.speed[1] = -ball.speed[1]

                  index_fewHit = ball.ballAction.collidelist(bricks.brickrect_fewHit)
                    # check if ball has hit wall
                    # if yes yhen delete brick and change ball direction
                  if index_fewHit != -1:
                        #self.brick_destroy_wav.play(0)
                        if ball.superBall != 1:
                            if ball.ballAction.center[0] > bricks.brickrect_fewHit[index_fewHit].right or \
                               ball.ballAction.center[0] < bricks.brickrect_fewHit[index_fewHit].left:
                                  if ball.ballAction.center[0] > bricks.brickrect_fewHit[index_fewHit].right:
                                        ball.ballAction.left = bricks.brickrect_fewHit[index_fewHit].right
                                        if ball.speed[0] == 0:
                                            ball.speed[0] = -3
                                        ball.speed[0] = -ball.speed[0]
                                  if ball.ballAction.center[0] < bricks.brickrect_fewHit[index_fewHit].left:
                                        ball.ballAction.right = bricks.brickrect_fewHit[index_fewHit].left
                                        if ball.speed[0] == 0:
                                            ball.speed[0] = 3
                                        ball.speed[0] = -ball.speed[0]

                            else:
                                if ball.ballAction.top > bricks.brickrect_fewHit[index_fewHit].top or \
                                    ball.ballAction.bottom < bricks.brickrect_fewHit[index_fewHit].bottom:
                                  self.text2 = font.render('x: ' + str(ball.ballAction.center[0]) + " Y: "+ str(bricks.brickrect_fewHit[index_fewHit].left), True, (255,255, 255))
                                  if ball.speed[1] < 0:
                                    ball.ballAction.top = bricks.brickrect_fewHit[index_fewHit].bottom
                                    ball.speed[1] = -ball.speed[1]
                                  else:
                                    ball.ballAction.bottom = bricks.brickrect_fewHit[index_fewHit].top
                                    ball.speed[1] = -ball.speed[1]
                        if bricks.brickrect_fewHitHits[index_fewHit] > 1:
                           bricks.brickrect_fewHitHits[index_fewHit] -=1
                        else:
                           self.bonus_array.append(bonus.Bonus(bricks.brickrect_fewHit[index_fewHit].left,bricks.brickrect_fewHit[index_fewHit].top,1))
                           bricks.brickrect_fewHitHits[index_fewHit:index_fewHit + 1] = []
                           bricks.brickrect_fewHit[index_fewHit:index_fewHit + 1] = []
                           self.points += 20 * self.point_multi
              mouse_pos = pygame.mouse.get_pos()



              text3 = font.render(u'uderzenie od lewego w: '+str(odrzut), True, (255,255, 255))

              if self.bonus_good_time > 0:
                if self.bonus_good_time == 1:
                   self.ball_catch_bonus = 0
                   for ball in self.balls_array:
                     ball.superBall = 0
                self.bonus_good_time=self.bonus_good_time-1
              if self.bonus_mad_time > 0:
                if self.bonus_mad_time == 1:
                  """"""
                self.bonus_mad_time=self.bonus_mad_time-1


              mousebutton = pygame.mouse.get_pressed()

              if mousebutton[0] == 1:
                  for ball in self.balls_array:
                    ball.go = 1


              if mousebutton[1] == 1:
                  if click == 1:
                      self.balls_array.append(self.ball(self))
                      self.balls_array[len(self.balls_array)-1].visible = 1
                      """for ball in self.balls_array:
                        ball.visible = 1
                        ball.go = 0"""
                      click = 0
              else:
                  click = 1
              if mousebutton[2] == 1:
                  for ball in self.balls_array:
                    ball.superBall = 1

              if (event.type == KEYDOWN):
                if (event.key == K_ESCAPE):
                    sys.exit(0)
                if (event.key == K_f):
                    if self.fullscreen == 0:
                        self.fullscreen = 1
                        self.screen = pygame.display.set_mode((size),FULLSCREEN)
                    else:
                        self.fullscreen = 0
                        self.screen = pygame.display.set_mode((size))
                if (event.key == K_s): 
                  for ball in self.balls_array:
                    ball.superBall = 1
                if (event.key == K_n):
                  if click == 1:
                      self.balls_array.append(self.ball(self))
                      self.balls_array[len(self.balls_array)-1].visible = 1
                      """for ball in self.balls_array:
                        ball.visible = 1
                        ball.go = 0"""
                      click = 0
                  else:
                      click = 1
                    
              self.screen.fill(color)
              #self.screen.blit(self.background, (0, 0))


              # Gorna forma z punktami
              pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, 20))
              good_time_text = font.render('Bonus 1: '+str(self.bonus_good_time/60)+' sek ', True, (255,255, 255))
              mad_time_text = font.render('Bonus 1: '+str(self.bonus_mad_time/60)+' sek', True, (255,255, 255))
              fps = font.render(" FPS: "+ str(round(clock.get_fps())), True, (255,255, 255))
              text = font.render('Klockow : '+str(len(bricks.brickrect)+len(bricks.brickrect_fewHit))+ "     Pilek: "+str(len(self.balls_array)), True, (255,255, 255))
              points_text = font.render('Punkty : '+str(self.points), True, (255,255, 255))
              lvl_text = font.render('Level : '+str(self.current_lvl+1), True, (255,255, 255))
              lives_text = font.render(u'Żyć : '+str(self.lives), True, (255,255, 255))

              self.screen.blit(good_time_text, (self.width - 300, 5))
              self.screen.blit(mad_time_text, (self.width - 400, 5))
              self.screen.blit(fps, (200, 5))
              self.screen.blit(text, (5, 5))
              self.screen.blit(points_text, (self.width - 150, 5))
              self.screen.blit(lvl_text, (self.width - 490, 5))
              self.screen.blit(lives_text, (self.width - 690, 5))

              for bonusa in self.bonus_array:
                  if bonusa.destruct == 0:
                      bonusa.show(self)
                      bonusa.action(self)

              for ball in self.balls_array:
                  ball.show(self)
              #screen.blit(dog, (a[0],a[1]))

              for i in range(0, len(bricks.brickrect)):
                    self.screen.blit(bricks.brick_img, bricks.brickrect[i])

              for i in range(0, len(bricks.brickrect_unbreake)):
                    self.screen.blit(bricks.brick_img_u, bricks.brickrect_unbreake[i])

              for i in range(0, len(bricks.brickrect_fewHit)):
                    self.screen.blit(bricks.brick_img_hit, bricks.brickrect_fewHit[i])

                    text_hit = self.font_brick.render(str(bricks.brickrect_fewHitHits[i]), True, (255,255, 255))
                    self.screen.blit(text_hit,(bricks.brickrect_fewHit[i][0]+20,bricks.brickrect_fewHit[i][1]+5))

              # PALETKA
              ik = ik+step
              if ik == 34: step=-step
              if ik == 0: step=-step
              if mouse_pos[1] < 458:
                  paddle_y_pos = 458
              else:
                  paddle_y_pos = mouse_pos[1]
              self.screen.blit(paddle[ik/7], (mouse_pos[0]-43, paddle_y_pos-15))
              pygame.display.flip()
