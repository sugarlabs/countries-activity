#!/usr/bin/python
# Countries.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g
import pygame
import utils
import sys
import load_save
import buttons
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import ctry
import letter_keys
import pages
import map1
import hint


class Countries:

    def __init__(self):
        self.journal = True  # set to False if we come in via main()
        self.canvas = None  # set to the pygame canvas if we come in via activity.py
        self.click_sound = pygame.mixer.Sound("data/sounds/clicksound.ogg")
        self.click_sound.set_volume(0.4)
        self.correct_ans_sound = pygame.mixer.Sound("data/sounds/correctans.ogg")
        self.wrong_ans_sound = pygame.mixer.Sound("data/sounds/wrongans.ogg")
        self.correct_ans_sound.set_volume(0.6)

    def display(self):
        if g.map1:
            self.map1.draw()
        elif g.pages:
            self.pages.draw()
        elif g.hint:
            self.hint.display()
        else:
            if g.offset > 0:
                g.screen.fill(utils.CREAM)
            g.screen.blit(g.bgd, g.xy0)
            utils.centre_blit(g.screen, g.pic, g.xyc)
            self.ctry.draw()
            if self.ctry.message is not None:
                utils.message1(
                    g.screen, g.font2, self.ctry.message, self.ctry.message_c)
        buttons.draw()

    def do_click(self):
        if g.map1:
            return False
        if g.hint:
            return False
        if g.pages:
            country = self.pages.which()
            if country is not None:
                self.map1.setup(country)
                self.map_on()
                return True
            return False
        l = self.ctry.which_oval()
        if l is not None:
            self.ctry.do_letter(l)
            return True
        else:
            if g.pic == g.globe:
                if self.ctry.complete():
                    if utils.mouse_on_img1(g.pic, g.xyc):
                        self.pages_on()
                        return True
            return False

    def pages_on(self):
        g.pages = True
        g.map1 = False
        buttons.on('blue')
        buttons.off(('clear', 'try', 'minus', 'space', 'replay', 'back', 'hint'))

    def map_on(self):
        g.map1 = True
        g.pages = False
        buttons.on('back')
        buttons.off(('fd', 'blue', 'bk'))
        buttons.off(('clear', 'try', 'minus', 'space', 'replay', 'hint'))

    def do_button(self, bu):
        if bu == 'back':
            self.pages_on()
            return
        if bu == 'try':
            value = self.ctry.try1()
            return value
        if bu == 'clear':
            self.ctry.clear()
            return
        if bu == 'replay':
            self.ctry.setup()
            return
        if bu == 'minus':
            self.do_key(pygame.K_MINUS)
            return
        if bu == 'space':
            self.do_key(pygame.K_SPACE)
            return
        if bu == 'fd':
            self.pages.fd()
            return
        if bu == 'bk':
            self.pages.bk()
            return
        if bu == 'blue':
            g.pages = False
            g.hint = False
            buttons.on(('clear', 'try', 'minus', 'space', 'replay', 'hint'))
            buttons.off(('fd', 'blue', 'bk', 'show'))
        if bu == 'hint':
            g.hint = True
            g.map1 = False
            g.pages = False
            buttons.off(('clear', 'try', 'minus', 'space', 'replay', 'back', 'hint'))
            buttons.on(('blue', 'show'))
        if bu == 'show':
            self.hint.get_country()

    def do_key(self, key):
        if key == pygame.K_1:
            g.version_display = not g.version_display
            return -1
        if key in g.TICK:
            value = self.ctry.try1()
            return value
        l = None
        if key in (pygame.K_BACKSPACE, pygame.K_DELETE):
            l = '*'
        else:
            l = letter_keys.which(key)
        if l is not None:
            self.ctry.do_letter(l)
            return -1
        if key == pygame.K_F1:
            self.pages_on()

        return -1

    def buttons_setup(self):
        cx1 = g.sx(1.5)
        cy1 = g.sy(1.5)
        cx2 = g.sx(32) - g.sy(1.5)
        cy2 = g.sy(19.8)
        buttons.Button('clear', (cx1, cy1), caption='clear', colour='yellow')
        buttons.Button('try', (cx2, cy2), caption='try', colour='yellow')
        buttons.Button('minus', (cx1, cy2), caption='dash', colour='yellow')
        buttons.Button('space', (cx1 + g.sy(3), cy2),
                       caption='space', colour='yellow')
        buttons.Button('replay', (cx2, cy1), caption='replay', colour='yellow')
        buttons.Button('hint', (cx2 - g.sy(3), cy2), caption='hint', colour='yellow')
        buttons.Button('show',(g.sx(23), cy2 - g.sy(12)), caption = 'show', colour = 'yellow')
        dx = g.sy(2.4)
        bx = g.sx(16) - dx
        by = g.sy(20.2)
        buttons.Button('bk', (bx, by), True)
        bx += dx
        buttons.Button('blue', (bx, by), True)
        bx += dx
        buttons.Button('fd', (bx, by), True)
        buttons.Button('back', (g.sx(2), g.sy(18)), True)
        buttons.off(('fd', 'blue', 'bk', 'back', 'show'))

    def flush_queue(self):
        flushing = True
        while flushing:
            flushing = False
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            for event in pygame.event.get():
                flushing = True


    def check_response(self):
        answer_fix = ctry.fix(self.ctry.answer)
        value, ans = self.ctry.check(answer_fix)
        l = ans[:1]
        ind = ord(l) - 65
        g.answers[ind] = ans
        self.ctry.flag(ans)
        ctry.text(l, answer_fix)
        self.ctry.message = "Good job, " + \
                            ans + " is the right answer!"
        self.correct_ans_sound.play()

    def proximity(self, up, down):
        if(up.pos[0] <= (down.pos[0] + 30) and up.pos[0] >= (down.pos[0] - 30)):
            if(up.pos[1] <= (down.pos[1] + 30) and up.pos[1] >= (down.pos[1] - 30)):
                return True
        return False

    def run(self):
        pygame.mixer.music.load("data/sounds/theme.ogg")
        pygame.mixer.music.play(-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.size, pygame.RESIZABLE)
                break

        g.init()
        if not self.journal:
            utils.load()
        self.pages = pages.Pages()
        self.map1 = map1.Map1()
        self.ctry = ctry.Ctry()
        self.hint = hint.Hint()
        load_save.retrieve()
        self.buttons_setup()
        if self.canvas is not None:
            self.canvas.grab_focus()
        ctrl = False
        going = True
        answer_input = False
        down_event = None

        while going:
            if self.journal:
                # Pump Gtk messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()
            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if not self.journal:
                        utils.save()
                    going = False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos = event.pos
                    g.redraw = True
                    if self.canvas is not None:
                        self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Store the latest MOUSEBUTTONDOWN event
                    self.click_sound.play()
                    if event.button == 1:
                        down_event = event
                elif event.type == pygame.MOUSEBUTTONUP:
                    g.redraw = True
                    self.ctry.message = None
                    g.pic = g.globe
                    if event.button == 1:
                        if self.proximity(event, down_event) and answer_input is False:
                            if self.do_click():
                                pass
                            else:
                                bu = buttons.check()
                                if bu != '':
                                    value = self.do_button(bu)
                                    if value == 0:
                                        answer_input = True    
                        elif self.proximity(event, down_event) and answer_input is True:
                            res = self.ctry.which_oval()
                            if res == 'y':
                                self.check_response()
                            else:
                                self.ctry.message = "Sorry, " + self.ctry.answer +\
                                                " is not on my list"
                            self.ctry.answer = ''
                            answer_input = False
                        self.flush_queue()
                    if event.button == 3:
                        self.ctry.clear()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    self.ctry.message = None
                    g.pic = g.globe
                    if ctrl:
                        if event.key == pygame.K_q:
                            if not self.journal:
                                utils.save()
                            going = False
                            break
                        else:
                            ctrl = False
                    if answer_input is False:
                        if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                            ctrl = True
                            break
                        value = self.do_key(event.key)
                        if value == 0:
                            answer_input = True
                    else:
                        if event.key == g.YES:  # Value of 'y'
                            self.check_response()
                        else:
                            
                            self.ctry.message = "Sorry, " + self.ctry.answer +\
                                                " is not on my list"
                            self.wrong_ans_sound.play()
                        self.ctry.answer = ''
                        answer_input = False
                    g.redraw = True
                    self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl = False
            if not going:
                break
            if g.redraw:
                self.display()
                if g.version_display:
                    utils.version_display()
                g.screen.blit(g.pointer, g.pos)
                pygame.display.flip()
                g.redraw = False
            g.clock.tick(40)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
    game = Countries()
    game.journal = False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
