import pygame
import g
import random
import os
import utils

class Hint:
    def __init__(self):
        self.img = None
        self.cxy = (g.sx(23), g.sy(5))
        self.ctry_idx = 0
        self.hint = ''
        self.ctry = ''
        self.text = 'Click Show button to get hint!'
        self.textxy = (g.sx(17),g.sy(15))
        self.flagxy = (g.sx(5),g.sy(2))

    def get_country(self):
        fname = os.path.join('data', 'countries.txt')
        f = open(fname, 'r')
        lines = f.readlines()
        self.ctry_idx = random.randint(0,len(lines)-1)
        self.img = pygame.image.load(f"data/flags/{self.ctry_idx}.png")
        self.img = pygame.transform.scale(self.img, (400, 300))
        self.ctry = lines[self.ctry_idx]
        self.ctry = self.ctry[:len(self.ctry)-1]
        self.hint = ''
        for i in range(0,len(self.ctry)):
            if i == 0:
                self.hint += self.ctry[i]
            elif self.ctry[i] == ' ':
                self.hint += ' '
            elif i == len(self.ctry) - 1:
                self.hint += self.ctry[i]
            elif i+1 < len(self.ctry) and self.ctry[i+1] == ',':
                self.hint += self.ctry[i]
                break
            else:
                self.hint += '*'

    def display(self):
        g.screen.fill((255,255,192))
        if(self.img):
            g.screen.blit(self.img,self.flagxy)
        utils.text_blit(
            g.screen,
            self.hint,
            g.font2,
            self.cxy,
            utils.BLACK,
            False)
        utils.text_blit(
            g.screen,
            self.text,
            g.font2,
            self.textxy,
            utils.BLACK,
            False)