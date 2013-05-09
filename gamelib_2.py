# To change this template, choose Tools | Templates
# and open the template in the editor.
# -*- coding: utf-8 -*-

import pygame
from pydoc import visiblename
import random
import brick
import sys


class game():
    class ball():
        visible = 1;
        monster = 0;
        def __init__(self, thisForm):
            self.speed=[5,5]
            self.ball=pygame.image.load("data/football.png")
            self.ballAction=self.ball.get_rect()
            #self.ballAction.left = (random.randint(0, thisForm.width))
            #self.ballAction.top = (random.randint(0, 200))
            self.go = 0

        def action(self, thisForm):
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] < 400:
                    paddle_y_pos = 400
            else:
                    paddle_y_pos = mouse_pos[1]
            if self.visible == 1:


              if self.go != 0:
                self.ballAction = self.ballAction.move(self.speed)
              else:
                
                self.ballAction.left = mouse_pos[0]+self.ballAction.bottom-self.ballAction.top+10-43
                self.ballAction.top = paddle_y_pos+self.ballAction.left-self.ballAction.right-15

              if self.ballAction.left < 0 or self.ballAction.right > thisForm.width:
                    self.speed[0] = -self.speed[0]
              if self.ballAction.top < 0:
                    self.speed[1] = -self.speed[1]
              if self.ballAction.top > thisForm.height:
                  self.visible = 0
                  print "koniec"
                  self.speed[1] = -self.speed[1]

              
              #zderzenie z paletka
              if self.ballAction.left > mouse_pos[0]-16-43 and self.ballAction.right < mouse_pos[0]+84+18-43 and self.ballAction.bottom < paddle_y_pos+30-15 and self.ballAction.bottom > paddle_y_pos-15:
                  if self.speed[1] > 0:
                    self.speed[1] = -self.speed[1]
                  odrzut = self.ballAction.left - mouse_pos[0]+16+43
                  self.speed[0] = -5 + odrzut/10 + random.randint(-1, 1)
        def show(self, thisForm):
            if self.visible == 1:
                thisForm.screen.blit(self.ball, self.ballAction)

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

    def __init__(self):
        pygame.init()
        size=self.width, self.height=1050, 780
        
        color=147,179,253
        self.screen=pygame.display.set_mode(size)

        
        dog=pygame.image.load("data/pies.gif")
        
        font = pygame.font.Font(None, 15)
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

        ball1= self.ball(self)
        ball2= self.ball(self)
        ball2.visible = 0
        ball3= self.ball(self)
        ball3.visible = 0

        bricks = brick.Brick("data/yellow_brick.png")

        bricks.build_wall(self.width)
        
        while True:
	  for event in pygame.event.get():
		  if event.type == pygame.QUIT: sys.exit()

          # 60 frames per second
          clock.tick(100)

          ''' Asuming your frames have a 16x16 size '''
          #explosion_images = self.load_sliced_sprites(20, 20, 'data/explosed-sprite.png')
          paddle = self.load_sliced_sprites(84, 24, 'data/ark.png')
          
          
	  ball1.action(self)
          ball2.action(self)
          ball3.action(self)
          
          
          
          index = ball1.ballAction.collidelist(bricks.brickrect)
          
            # check if ball has hit wall
            # if yes yhen delete brick and change ball direction
          if index != -1:
                if ball1.monster != 1:
                    if ball1.ballAction.center[0] > bricks.brickrect[index].right or \
                       ball1.ballAction.center[0] < bricks.brickrect[index].left:
                        ball1.speed[0] = -ball1.speed[0]
                    else:
                        ball1.speed[1] = -ball1.speed[1]
                bricks.brickrect[index:index + 1] = []

          index = ball2.ballAction.collidelist(bricks.brickrect)
          if index != -1:
                if ball2.monster != 1:
                    if ball2.ballAction.center[0] > bricks.brickrect[index].right or \
                       ball2.ballAction.center[0] < bricks.brickrect[index].left:
                        ball2.speed[0] = -ball2.speed[0]
                    else:
                        ball2.speed[1] = -ball2.speed[1]
                bricks.brickrect[index:index + 1] = []

          index = ball3.ballAction.collidelist(bricks.brickrect)
          if index != -1:
                if ball3.monster != 1:
                    if ball3.ballAction.center[0] > bricks.brickrect[index].right or \
                       ball3.ballAction.center[0] < bricks.brickrect[index].left:
                        ball3.speed[0] = -ball3.speed[0]
                    else:
                        ball3.speed[1] = -ball3.speed[1]
                bricks.brickrect[index:index + 1] = []
          mouse_pos = pygame.mouse.get_pos()
          text = font.render(u'TEST: '+str(len(bricks.brickrect)), True, (255,255, 255))
          
          text2 = font.render(u'mouse X: '+str(mouse_pos[0])+'mouse Y: '+str(mouse_pos[1]), True, (255,255, 255))
          text3 = font.render(u'uderzenie od lewego w: '+str(odrzut), True, (255,255, 255))

          mousebutton = pygame.mouse.get_pressed()

          if mousebutton[0] == 1:
              ball1.go = 1
              ball2.go = 1
              ball3.go = 1

          if mousebutton[1] == 1:
              ball1.visible = 1
              ball1.go = 0
              ball2.visible = 1
              ball2.go = 0
              ball3.visible = 1
              ball3.go = 0

          if mousebutton[2] == 1:
              ball1.monster = 1
              ball2.monster = 1
              ball3.monster = 1
          else:
              ball1.monster = 0
              ball2.monster = 0
              ball3.monster = 0
          # WYPElNIENIE
	  self.screen.fill(color)


          
          
	  ball1.show(self)
          ball2.show(self)
          ball3.show(self)
          #screen.blit(dog, (a[0],a[1]))
          self.screen.blit(text, (5, 5))
          for i in range(0, len(bricks.brickrect)):
                self.screen.blit(bricks.brick_img, bricks.brickrect[i])




          # TEXTY
          self.screen.blit(text2, (5, 20))
          self.screen.blit(text3, (5, 40))

          # PALETKA
          ik = ik+step
          if ik == 34: step=-step
          if ik == 0: step=-step
          if mouse_pos[1] < 400:
              paddle_y_pos = 400
          else:
              paddle_y_pos = mouse_pos[1]
          self.screen.blit(paddle[ik/7], (mouse_pos[0]-43, paddle_y_pos-15))
	  pygame.display.flip()
