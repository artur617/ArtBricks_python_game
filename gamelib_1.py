# To change this template, choose Tools | Templates
# and open the template in the editor.
# -*- coding: utf-8 -*-

import pygame
import random


class game():
    class ball(self):
        def __init__(self):
            ball=pygame.image.load("data/football.png")
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
        size=width, height=1050, 780
        speed=[5,5]
        color=147,179,253
        screen=pygame.display.set_mode(size)

        
        dog=pygame.image.load("data/pies.gif")
        ballAction=ball.get_rect()
        font = pygame.font.Font(None, 15)
        odrzut = 0
        pygame.mouse.set_visible(False)
        i = 0
        step = 1

        ballAction.left = (random.randint(0, width))
        ballAction.top = (random.randint(0, 200))
        
        while True:
	  for event in pygame.event.get():
		  if event.type == pygame.QUIT: sys.exit()
                  
          ''' Asuming your frames have a 16x16 size '''
          #explosion_images = self.load_sliced_sprites(20, 20, 'data/explosed-sprite.png')
          paddle = self.load_sliced_sprites(84, 24, 'data/ark.png')
          
          
	  ballAction = ballAction.move(speed)

	  if ballAction.left < 0 or ballAction.right > width:
	   	speed[0] = -speed[0]
	  if ballAction.top < 0:
		  speed[1] = -speed[1]
          if ballAction.bottom > height:
              print "koniec"
              speed[1] = -speed[1]

          mouse_pos = pygame.mouse.get_pos()


          #zderzenie z paletka
          if ballAction.left > mouse_pos[0]-16 and ballAction.right < mouse_pos[0]+84+18 and ballAction.bottom < mouse_pos[1]+30 and ballAction.bottom > mouse_pos[1]:
              if speed[1] > 0:
                speed[1] = -speed[1]
              odrzut = ballAction.left - mouse_pos[0]+16
              speed[0] = -5 + odrzut/10 + random.randint(-1, 1)
              
              
          text = font.render(u'X L: '+str(ballAction.left)+'X R: '+str(ballAction.right)+'Y T: '+str(ballAction.top)+'Y B: '+str(ballAction.bottom), True, (255,255, 255))
          
          text2 = font.render(u'mouse X: '+str(mouse_pos[0])+'mouse Y: '+str(mouse_pos[1]), True, (255,255, 255))
          text3 = font.render(u'uderzenie od lewego w: '+str(odrzut), True, (255,255, 255))

	  screen.fill(color)
	  screen.blit(ball, ballAction)
          #screen.blit(dog, (a[0],a[1]))
          screen.blit(text, (5, 5))
          screen.blit(text2, (5, 20))
          screen.blit(text3, (5, 40))
          i = i+step
          if i == 34: step=-step
          if i == 0: step=-step
          screen.blit(paddle[i/7], (mouse_pos[0], mouse_pos[1]))
	  pygame.display.flip()
