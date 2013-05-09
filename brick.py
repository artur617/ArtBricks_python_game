import random
import pygame

class Brick():
    def __init__(self, image):
        self.brick_img = pygame.image.load(image).convert_alpha()
        
        self.rect = self.brick_img.get_rect()
        self.bricklength = self.rect.right - self.rect.left
        self.brickheight = self.rect.bottom - self.rect.top
    def update(self, ball, screen):
        screen.blit(self.brick_img, (200,200))

    def build_simple_level(self, string, width):
        self.brickrect = []
        self.brickrect_unbreake = []
        self.brickrect_fewHit = []
        self.brickrect_fewHitHits = []

        xpos = 2
        ypos = 22
        adj = 0

        for block in string:
            if xpos > width-15:
                if adj == 0:
                    """adj = self.bricklength / 2"""
                else:
                    adj = 0
                xpos = 2
                ypos += 17+3
            
            if block == "O":
                self.buildSimpleBrick(xpos, ypos)
            if block == "X":
                self.buildUnbrekableBrick(xpos, ypos)
            if block > "0" and block <= "9":
                self.buildFewHitBrick(xpos, ypos, block)
            if block == "0":
                self.buildFewHitBrick(xpos, ypos, 10)
            xpos = xpos + 50+1

    def buildUnbrekableBrick(self,xpos, ypos):
        self.brick_img_u = pygame.image.load("data/unbreak_brick.png").convert_alpha()
        self.brickrect_unbreake.append(self.brick_img_u.get_rect())
        self.brickrect_unbreake[len(self.brickrect_unbreake)-1] = self.brickrect_unbreake[len(self.brickrect_unbreake)-1].move(xpos, ypos)

    def buildSimpleBrick(self,xpos, ypos):
        self.brick_img = pygame.image.load("data/green_brick.png").convert_alpha()
        self.brickrect.append(self.brick_img.get_rect())
        self.brickrect[len(self.brickrect)-1] = self.brickrect[len(self.brickrect)-1].move(xpos, ypos)

    def buildFewHitBrick(self,xpos, ypos, hits):
        self.brick_img_hit = pygame.image.load("data/blue_brick.png").convert_alpha()
        self.brickrect_fewHit.append(self.brick_img_hit.get_rect())
        self.brickrect_fewHit[len(self.brickrect_fewHit)-1] = self.brickrect_fewHit[len(self.brickrect_fewHit)-1].move(xpos, ypos)
        self.brickrect_fewHitHits.append(int(hits))

    def build_wall(self, width):
        xpos = 2
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 100):
            if xpos > width-15:
                if adj == 0:
                    """adj = self.bricklength / 2"""
                else:
                    adj = 0
                xpos = 2
                ypos += self.brickheight+3

            self.brickrect.append(self.brick_img.get_rect())
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength +1

    def build_wall_unbreake(self, width):
        self.brick_img_u = pygame.image.load("data/unbreak_brick.png").convert_alpha()

        self.rect_u = self.brick_img_u.get_rect()
        self.bricklength_unbreake = self.rect_u.right - self.rect_u.left
        self.brickheight_unbreake = self.rect_u.bottom - self.rect_u.top

        xpos = 2
        ypos = 260
        adj = 0
        self.brickrect_unbreake = []
        for i in range (0, 0):
            if xpos > width-15:
                if adj == 0:
                    """adj = self.bricklength / 2"""
                else:
                    adj = 0
                xpos = 2
                ypos += self.brickheight_unbreake+3

            self.brickrect_unbreake.append(self.brick_img_u.get_rect())
            self.brickrect_unbreake[i] = self.brickrect_unbreake[i].move(xpos, ypos)
            xpos = xpos + self.bricklength_unbreake*  3


    def build_wall_fewHit(self, width):
        self.brick_img_hit = pygame.image.load("data/blue_brick.png").convert_alpha()

        self.rect_u = self.brick_img_u.get_rect()
        self.bricklength_fewHit = self.rect_u.right - self.rect_u.left
        self.brickheight_fewHit = self.rect_u.bottom - self.rect_u.top
        self.hits = 2
        

        xpos = 2
        ypos = 260
        adj = 0
        self.brickrect_fewHit = []
        self.brickrect_fewHitHits = []
        for i in range (0, 40):
            if xpos > width-15:
                if adj == 0:
                    """adj = self.bricklength / 2"""
                else:
                    adj = 0
                xpos = 2
                ypos += self.brickheight_fewHit+3

            self.brickrect_fewHit.append(self.brick_img_u.get_rect())
            self.brickrect_fewHit[i] = self.brickrect_fewHit[i].move(xpos, ypos)
            self.brickrect_fewHitHits.append(self.hits)
            xpos = xpos + self.bricklength_fewHit+1