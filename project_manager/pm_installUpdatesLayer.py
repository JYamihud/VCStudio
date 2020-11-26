# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os
import sys
import urllib3

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
        200,
        10)
    
    # Title of the operation. Incase the user forgot. 
    UI_elements.text(layer, win, "installing_project_title",
        win.current["w"]/2-250,
        win.current["h"]/2-15,
        500,
        30,
        10,
        fill=False,
        centered=True,
        editable=False)
    
    win.text["installing_project_title"]["text"] = talk.text("update_installing")
    
    frame = win.current["frame"] - win.update["frame"] - 50
    files = win.update["get_files"]
    
    UI_color.set(layer, win, "progress_background")
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2-200,
        win.current["h"]/2+70,
        400,
        20,
        10)
    
    if frame in range(-1, len(files)):
        
        filename = files[frame]
        
        try:
            UI_color.set(layer, win, "text_normal")
            layer.set_font_size(15)
            layer.move_to(win.current["w"]/2-(len(files[frame+1])*9)/2,
                win.current["h"]/2+50)
            layer.show_text(files[frame+1])
        except:
            pass    
        
        path = "https://notabug.org/jyamihud/VCStudio/raw/master/"
        url = path+filename
        
        http = urllib3.PoolManager()
        r = http.request('GET', url, preload_content=False)
        with open(filename, 'wb') as out:
            while True:
                data = r.read(1024)
                if not data:
                    break
                out.write(data)

        r.release_conn()
        
    
    fraction = ((frame + 1) / len(files))
    if fraction > 1:
        fraction = 1
    
    UI_color.set(layer, win, "progress_active")
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2-200,
        win.current["h"]/2+70,
        (400)*fraction,
        20,
        10)

    if frame > len(files)+30:
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    return surface
