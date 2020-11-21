# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os

# GTK module ( Graphical interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk
import cairo

# Own modules
from settings import settings
from settings import talk
from project_manager import pm_project

#UI modules
from UI import UI_elements
from UI import UI_color


def layer(win):
    
    # Making the layer
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, win.current['w'],
                                                      win.current['h'])
    layer = cairo.Context(surface)
    
    
    #text setting
    layer.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    
    UI_color.set(layer, win, "dark_overdrop")
    layer.rectangle(
        0,
        0,
        win.current["w"],
        win.current["h"],
        )
    layer.fill()
    
    # So it's going to be like a little window in the center of the VCStudio
    # with a simple UI. Probably like 2 things. Folder and a projectname.
    
    UI_color.set(layer, win, "node_background")
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2-250,
        win.current["h"]/2-50,
        500,
        100,
        10)
    
    # Title of the operation. Incase the user forgot. 
    UI_elements.text(layer, win, "scan_project_title",
        win.current["w"]/2-250,
        win.current["h"]/2-15,
        500,
        30,
        10,
        fill=False,
        centered=True,
        editable=False)
    
    win.text["scan_project_title"]["text"] = talk.text("duringscanningforprojects")
    
    blur = UI_elements.animate("project_manager_blur", win)
    
    if blur > 49:
        pm_project.scan()
        win.url = "project_manager"
    
    return surface
