#!/usr/bin/python
# Countries.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,load_save,buttons
try:
    import gtk
except:
    pass
import ctry,letter_keys,pages,map1

class Countries:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        if g.map1:
            self.map1.draw()
        elif g.pages:
            self.pages.draw()
        else:
            if g.offset>0: g.screen.fill(utils.CREAM)
            g.screen.blit(g.bgd,g.xy0)
            utils.centre_blit(g.screen,g.pic,g.xyc)
            self.ctry.draw()
            if self.ctry.message!=None:
                utils.message1(\
                    g.screen,g.font2,self.ctry.message,self.ctry.message_c)
        buttons.draw()

    def do_click(self):
        if g.map1: return False
        if g.pages:
            country=self.pages.which()
            if country!=None:
                self.map1.setup(country); self.map_on()
                return True
            return False
        l=self.ctry.which_oval()
        if l!=None:
            self.ctry.do_letter(l); return True
        else:
            if g.pic==g.globe:
                if self.ctry.complete():
                    if utils.mouse_on_img1(g.pic,g.xyc):
                        self.pages_on()
                        return True
            return False

    def pages_on(self):
        g.pages=True; g.map1=False
        buttons.on('blue')
        buttons.off(('clear','try','minus','space','replay','back'))
        
    def map_on(self):
        g.map1=True; g.pages=False
        buttons.on('back')
        buttons.off(('fd','blue','bk'))
        buttons.off(('clear','try','minus','space','replay'))
        
    def do_button(self,bu):
        if bu=='back': self.pages_on(); return
        if bu=='try': self.ctry.try1(); return
        if bu=='clear': self.ctry.clear(); return
        if bu=='replay': self.ctry.setup(); return
        if bu=='minus': self.do_key(pygame.K_MINUS); return
        if bu=='space': self.do_key(pygame.K_SPACE); return
        if bu=='fd': self.pages.fd(); return
        if bu=='bk': self.pages.bk(); return
        if bu=='blue':
            g.pages=False
            buttons.on(('clear','try','minus','space','replay'))
            buttons.off(('fd','blue','bk'))

    def do_key(self,key):
        if key==pygame.K_1: g.version_display=not g.version_display; return
        if key in g.TICK: self.ctry.try1(); return
        l=None
        if key in (pygame.K_BACKSPACE,pygame.K_DELETE): l='*'
        else: l=letter_keys.which(key)
        if l!=None: self.ctry.do_letter(l); return
        if key==pygame.K_F1: self.pages_on()

    def buttons_setup(self):
        cx1=g.sx(1.5); cy1=g.sy(1.5); cx2=g.sx(32)-g.sy(1.5); cy2=g.sy(19.8)
        buttons.Button('clear',(cx1,cy1),caption='clear',colour='yellow')
        buttons.Button('try',(cx2,cy2),caption='try',colour='yellow')
        buttons.Button('minus',(cx1,cy2),caption='dash',colour='yellow')
        buttons.Button('space',(cx1+g.sy(3),cy2),caption='space',colour='yellow')
        buttons.Button('replay',(cx2,cy1),caption='replay',colour='yellow')
        dx=g.sy(2.4); bx=g.sx(16)-dx; by=g.sy(20.2)
        buttons.Button('bk',(bx,by),True); bx+=dx
        buttons.Button('blue',(bx,by),True); bx+=dx
        buttons.Button('fd',(bx,by),True)
        buttons.Button('back',(g.sx(2),g.sy(18)),True)
        buttons.off(('fd','blue','bk','back'))

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.pages=pages.Pages()
        self.map1=map1.Map1()
        self.ctry=ctry.Ctry()
        load_save.retrieve()
        self.buttons_setup()
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    self.ctry.message=None; g.pic=g.globe
                    if event.button==1:
                        if self.do_click():
                            pass
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu)
                        self.flush_queue()
                    if event.button==3: self.ctry.clear()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        self.ctry.message=None; g.pic=g.globe
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
    game=Countries()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
