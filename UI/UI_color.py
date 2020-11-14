# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os
import math

# GTK module ( Graphical interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo

# Own modules
from settings import settings
from settings import talk

def get_table():
    
    # This function will give a whole table of colors from a theme. So there will
    # be no need to read from the theme.data file every time we need a color of
    # somethings. It would've been stupid. So we load all the colors into RAM
    # at this stage. Similar stuff should be done with talk.text() i guess.
    
    # First let's find what is actually the theme we are using.
    try:
        data = open("settings/themes/"+settings.read("Theme")+"/theme.data")
    except:
        # If by any change it fails to read the theme from the Theme setting
        # it will use the Default theme.
        data = open("settings/themes/Default/theme.data")
        settings.write("Theme", "Default")
    
    data = data.read()
    data = data.split("\n")
    
    # Parsing
    ret = {}
    for d in data:
        if d:
            name = d.split(" = ")[0]
            color = d.split(" = ")[1].split(",")
            c = []
            for co in color:
                try:
                    c.append(float(co))
                except:
                    c.append(0.0)
            color = c
            ret[name] = color
    # Returning
    return ret

def set(layer, win, color):
    # One line code less to setup a color each time LOL
    try:
        r,g,b,a = win.color[color]
        layer.set_source_rgba(r,g,b,a)
    except:
        layer.set_source_rgba(1,0,1,1)
