# activity.py
# my standard link between sugar and my activity

from gettext import gettext as _
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import pygame
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.style import GRID_CELL_SIZE
import sugargame.canvas
import load_save
import Countries
import ctry
import pages
import map1
import buttons
import g


class PeterActivity(activity.Activity):
    def __init__(self, handle):
        super(PeterActivity, self).__init__(handle)

        # Build the activity toolbar.
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        self.show_all()

        # Create the game instance.
        self.game = Countries.Countries()

        # Build the Pygame canvas.
        self.game.canvas = self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display, pygame.font])
        # Note that set_canvas implicitly calls
        # read_file when resuming from the Journal.
        self.set_canvas(self._pygamecanvas)

        Gdk.Screen.get_default().connect('size-changed',
                                         self.__configure_cb)

    def read_file(self, file_path):
        try:
            f = open(file_path, 'r')
        except BaseException:
            return  # ****
        load_save.load(f)
        f.close()

    def write_file(self, file_path):
        f = open(file_path, 'w')
        load_save.save(f)
        f.close()

    def __configure_cb(self, event):
        ''' Screen size has changed '''
        pygame.display.set_mode((Gdk.Screen.width(),
                                 Gdk.Screen.height() - GRID_CELL_SIZE),
                                 pygame.RESIZABLE)
        g.init()
        self.game.ctry = ctry.Ctry()
        self.game.pages = pages.Pages()
        self.game.map1 = map1.Map1()
        buttons.deactive()
        self.game.buttons_setup()
