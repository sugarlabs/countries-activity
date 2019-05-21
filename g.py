# g.py - globals
import pygame
import utils
import random
import ctry

app = 'Countries'
ver = '1'
ver = '21'
ver = '22'
# replay button - extra flags
ver = '23'
# allows overwriting - extra flags & countries
ver = '24'
# flag files use numbers instead of names - as per order in countries.txt
# dynamically works out the missing letters - W & X in English
ver = '25'
# flag files fixed
# flushing improved
ver = '26'
# 18 flags changed - 21 countries added
# exact names used throughout
ver = '27'
# Romania flag updated
# Replaced Congo with Democratic Republic of the Congo
#    and Republic of the Congo
ver = '28'
# added index.html to data/flags
ver = '29'
# dropped index.html - added pages idea
ver = '30'
# alternative names in CSV form
# clickable flags
ver = '31'
# capital/lat-long intercahnged
ver = '32'
# Equirectangular projection map
ver = '33'
# countries.txt & latlon.txt rationalised
# dash instead of minus
YES = 121
UP = (264, 273)
DOWN = (258, 274)
LEFT = (260, 276)
RIGHT = (262, 275)
CROSS = (259, 120)
CIRCLE = (265, 111)
SQUARE = (263, 32)
TICK = (257, 13)
NUMBERS = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4,
           pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8,
           pygame.K_9: 9, pygame.K_0: 0}


def init():  # called by run()
    random.seed()
    global redraw
    global screen, w, h, font0, font1, font2, clock
    global factor, offset, imgf, message, version_display
    global pos, pointer
    redraw = True
    version_display = False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill(utils.CREAM)
    pygame.display.flip()
    w, h = screen.get_size()
    if float(w) / float(h) > 1.5:  # widescreen
        offset = (w - 4 * h / 3) / 2  # we assume 4:3 - centre on widescreen
    else:
        h = int(.75 * w)  # allow for toolbar - works to 4:3
        offset = 0
    factor = float(h) / 24  # measurement scaling factor (32x24 = design units)
    # image scaling factor - all images built for 1200x900
    imgf = float(h) / 900
    clock = pygame.time.Clock()
    if pygame.font:
        t = int(30 * imgf)
        font0 = pygame.font.Font(None, t)
        t = int(40 * imgf)
        font1 = pygame.font.Font(None, t)
        t = int(60 * imgf)
        font2 = pygame.font.Font(None, t)
    message = ''
    pos = pygame.mouse.get_pos()
    pointer = utils.load_image('pointer.png', True)
    pygame.mouse.set_visible(False)

    # this activity only
    global answers, bgd, xy0, globe, xyc, pic, pages, countries, map1
    xy0 = (sx(0), sy(0))
    globe = utils.load_image('globe.png', True)
    xyc = (sx(16), sy(9))
    pages = False
    countries = None
    map1 = False


def sx(f):  # scale x function
    return int(f * factor + offset + .5)


def sy(f):  # scale y function
    return int(f * factor + .5)
