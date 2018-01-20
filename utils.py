# utils.py
import g
import pygame
import sys
import os
import random
import copy
import load_save

# constants
RED, BLUE, GREEN, BLACK, WHITE = (
    255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0), (255, 255, 255)
CYAN, ORANGE, CREAM, YELLOW = (
    0, 255, 255), (255, 165, 0), (255, 255, 192), (255, 255, 0)
MAGENTA = (255, 0, 255)


def exit():
    save()
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def save():
    dir = ''
    dir = os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir is None:
        dir = ''
    fname = os.path.join(dir, 'data', 'Countries.dat')
    f = open(fname, 'w')
    load_save.save(f)
    f.close


def load():
    dir = ''
    dir = os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir is None:
        dir = ''
    fname = os.path.join(dir, 'data', 'Countries.dat')
    try:
        f = open(fname, 'r')
    except BaseException:
        return None  # ****
    try:
        load_save.load(f)
    except BaseException:
        pass
    f.close


def version_display():
    g.message = g.app + ' ' + g.ver
    g.message += '  ' + str(g.screen.get_width()) + \
        ' x ' + str(g.screen.get_height())
    message(g.screen, g.font1, g.message)

# loads an image (eg pic.png) from the data subdirectory
# converts it for optimum display
# resizes it using the image scaling factor, g.imgf
#   so it is the right size for the current screen resolution
#   all images are designed for 1200x900


def load_image(file1, alpha=False, subdir=''):  # eg subdir='glow'
    data = 'data'
    if subdir != '':
        data = os.path.join('data', subdir)
    fname = os.path.join(data, file1)
    try:
        img = pygame.image.load(fname)
    except BaseException:
        print "Peter says: Can't find " + fname
        exit()
    if alpha:
        img = img.convert_alpha()
    else:
        img = img.convert()
    if abs(g.imgf - 1.0) > .1:  # only scale if factor <> 1
        w = img.get_width()
        h = img.get_height()
        try:
            img = pygame.transform.smoothscale(
                img, (int(g.imgf * w), int(g.imgf * h)))
        except BaseException:
            img = pygame.transform.scale(
                img, (int(g.imgf * w), int(g.imgf * h)))
    return img

# eg new_list=copy_list(old_list)


def copy_list(l):
    new_list = []
    new_list.extend(l)
    return new_list


def shuffle(lst):
    l1 = lst
    lt = []
    for i in range(len(lst)):
        ln = len(l1)
        r = random.randint(0, ln - 1)
        lt.append(lst[r])
        l1.remove(lst[r])
    return lt


def centre_blit(screen, img, xxx_todo_changeme, angle=0):  # rotation is clockwise
    (cx, cy) = xxx_todo_changeme
    img1 = img
    if angle != 0:
        img1 = pygame.transform.rotate(img, -angle)
    rect = img1.get_rect()
    screen.blit(img1, (cx - rect.width / 2, cy - rect.height / 2))


def text_blit(
        screen,
        s,
        font,
        xxx_todo_changeme1,
        xxx_todo_changeme2,
        shadow=True):
    (cx, cy) = xxx_todo_changeme1
    (r, g, b) = xxx_todo_changeme2
    if shadow:
        text = font.render(s, True, (0, 0, 0))
        rect = text.get_rect()
        rect.centerx = cx + 2
        rect.centery = cy + 2
        screen.blit(text, rect)
    text = font.render(s, True, (r, g, b))
    rect = text.get_rect()
    rect.centerx = cx
    rect.centery = cy
    screen.blit(text, rect)
    return rect


def text_blit1(
        screen,
        s,
        font,
        xxx_todo_changeme3,
        xxx_todo_changeme4,
        shadow=True):
    (x, y) = xxx_todo_changeme3
    (r, g, b) = xxx_todo_changeme4
    if shadow:
        text = font.render(s, True, (0, 0, 0))
        rect = text.get_rect()
        rect.x = x + 2
        rect.y = y + 2
        screen.blit(text, rect)
    text = font.render(s, True, (r, g, b))
    rect = text.get_rect()
    rect.x = x
    rect.y = y
    screen.blit(text, rect)
    return rect

# m is the message
# d is the # of pixels in the border around the text
# (cx,cy) = co-ords centre - (0,0) means use screen centre


def message(screen, font, m, xxx_todo_changeme5=(0, 0), d=20):
    (cx, cy) = xxx_todo_changeme5
    if m != '':
        if pygame.font:
            text = font.render(m, True, (255, 255, 255))
            shadow = font.render(m, True, (0, 0, 0))
            rect = text.get_rect()
            if cx == 0:
                cx = screen.get_width() / 2
            if cy == 0:
                cy = screen.get_height() / 2
            rect.centerx = cx
            rect.centery = cy
            bgd = pygame.Surface((rect.width + 2 * d, rect.height + 2 * d))
            bgd.fill((0, 255, 255))
            bgd.set_alpha(128)
            screen.blit(bgd, (rect.left - d, rect.top - d))
            screen.blit(
                shadow,
                (rect.x + 2,
                 rect.y + 2,
                 rect.width,
                 rect.height))
            screen.blit(text, rect)


def message1(screen, font, m, xxx_todo_changeme6, d=15):
    (cx, cy) = xxx_todo_changeme6
    text = font.render(m, True, ORANGE)
    rect = text.get_rect()
    rect.centerx = cx
    rect.centery = cy
    bgd = pygame.Surface((rect.width + 2 * d, rect.height + 2 * d))
    bgd.fill(BLUE)
    screen.blit(bgd, (rect.left - d, rect.top - d))
    screen.blit(text, rect)


def mouse_on_img(img, xxx_todo_changeme7):  # x,y=top left
    (x, y) = xxx_todo_changeme7
    w = img.get_width()
    h = img.get_height()
    mx, my = g.pos
    if mx < x:
        return False
    if mx > (x + w):
        return False
    if my < y:
        return False
    if my > (y + h):
        return False
    try:  # in case out of range
        col = img.get_at((int(mx - x), int(my - y)))
    except BaseException:
        return False
    if col[3] < 10:
        return False
    return True


def mouse_on_img1(img, xxx_todo_changeme8):
    (cx, cy) = xxx_todo_changeme8
    xy = centre_to_top_left(img, (cx, cy))
    return mouse_on_img(img, xy)


def mouse_on_img_rect(img, xxx_todo_changeme9):
    (cx, cy) = xxx_todo_changeme9
    w2 = img.get_width() / 2
    h2 = img.get_height() / 2
    x1 = cx - w2
    y1 = cy - h2
    x2 = cx + w2
    y2 = cy + h2
    return mouse_in(x1, y1, x2, y2)


def mouse_in(x1, y1, x2, y2):
    mx, my = g.pos
    if x1 > mx:
        return False
    if x2 < mx:
        return False
    if y1 > my:
        return False
    if y2 < my:
        return False
    return True


def mouse_in_rect(rect):  # x,y,w,h
    return mouse_in(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])


def display_score():
    if pygame.font:
        text = g.font2.render(str(g.score), True, ORANGE, BLUE)
        w = text.get_width()
        h = text.get_height()
        x = g.sx(5.7)
        y = g.sy(18.8)
        d = g.sy(.3)
        pygame.draw.rect(
            g.screen,
            BLUE,
            (x - d - g.sy(.05),
             y - d,
             w + 2 * d,
             h + 2 * d))
        g.screen.blit(text, (x, y))
        centre_blit(
            g.screen,
            g.sparkle,
            (x - d + g.sy(.05),
             y + h / 2 - g.sy(.2)))


def display_number(
        n,
        xxx_todo_changeme10,
        font,
        colour=BLACK,
        bgd=None,
        outline_font=None):
    (cx, cy) = xxx_todo_changeme10
    if pygame.font:
        if bgd is None:
            text = font.render(str(n), True, colour)
        else:
            text = font.render(str(n), True, colour, bgd)
        if outline_font is not None:
            outline = outline_font.render(str(n), True, BLACK)
            centre_blit(g.screen, outline, (cx, cy))
        centre_blit(g.screen, text, (cx, cy))


def display_number1(n, xxx_todo_changeme11, font, colour=BLACK):
    (x, cy) = xxx_todo_changeme11
    if pygame.font:
        text = font.render(str(n), True, colour)
        y = cy - text.get_height() / 2
        g.screen.blit(text, (x, y))


def display_number2(screen, n, xxx_todo_changeme12, font, colour=BLACK):
    (cx, cy) = xxx_todo_changeme12
    if pygame.font:
        text = font.render(str(n), True, colour)
        centre_blit(screen, text, (cx, cy))


def display_number3(screen, n, xxx_todo_changeme13, font, colour=BLACK):
    (x, y) = xxx_todo_changeme13
    if pygame.font:
        lead = 0
        if n < 10:
            one = font.render('1', True, colour)
            lead = one.get_width()
        s = str(n)
        text = font.render(s, True, colour)
        screen.blit(text, (lead + x, y))


def top_left_to_centre(img, xxx_todo_changeme14):
    (x, y) = xxx_todo_changeme14
    cx = x + img.get_width() / 2
    cy = y + img.get_height() / 2
    return (cx, cy)


def centre_to_top_left(img, xxx_todo_changeme15):
    (cx, cy) = xxx_todo_changeme15
    x = cx - img.get_width() / 2
    y = cy - img.get_height() / 2
    return (x, y)


def sign(n):
    if n < 0:
        return -1
    return 1


def avg(c1, c2):
    (x1, y1) = c1
    (x2, y2) = c2
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    return (x, y)


def ch_set(s, ind, ch):  # eg ch_set('abc',1,'x')->'axc'
    return s[:ind] + ch + s[(ind + 1):]


def initcap(s):
    s = s.lstrip()
    s = s.rstrip()
    s = s.capitalize()
    t = ''
    space = False
    for ch in s:
        if space:
            if ch == ' ':
                ch = ''
            else:
                ch = ch.capitalize()
                space = False
        if ch == ' ':
            space = True
        t += ch
    return t
