# THIS FILE IS A PART OF VCStudio
# PYTHON 3

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
        100,
        500,
        win.current["h"]-200,
        10)
    
    # Exit button
    def do():
        win.url = "project_manager" 
        win.textactive = ""
        
        
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2+210,
        win.current["h"]-140,
        40,
        40,
        10,
        button=do,
        icon="cancel",
        tip=talk.text("cancel"))
    
    # Install Updates button
    try:
        if win.update["count"]:
            def do():
                win.url = "install_updates"
                win.update["frame"] = win.current["frame"]
                
                
            UI_elements.roundrect(layer, win, 
                win.current["w"]/2+170,
                win.current["h"]-140,
                40,
                40,
                10,
                button=do,
                icon="ok",
                tip=talk.text("update_install"))
    except:
        pass       
        
    # Clipping everything
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2-250,
        100,
        500,
        win.current["h"]-260,
        10,
        fill=False)
    layer.clip()
    
    clip = [
        win.current["w"]/2-250,
        100,
        500,
        win.current["h"]-260]
    
    # Setting up the scroll
    if "pm_update" not in win.scroll:
        win.scroll["pm_update"] = 0
    
    current_Y = 0 # The max scroll value
    
    for version in win.update["versions"]:
        is_open = win.update["versions"][version]["open"]
        files   = win.update["versions"][version]["files"]
        link    = win.update["versions"][version]["link"]
        
        
        if version == win.version:
            UI_color.set(layer, win, "node_imagefile")
            sufix = talk.text("update_current")
        elif version < win.version:
            UI_color.set(layer, win, "node_badfile")
            sufix = talk.text("update_previous")
        elif version > win.version:
            UI_color.set(layer, win, "node_blendfile")
            sufix = talk.text("update_available")
        
        UI_elements.roundrect(layer, win, 
            win.current["w"]/2-240,
            110 + current_Y + win.scroll["pm_update"],
            450,
            40,
            10)
        
        UI_color.set(layer, win, "text_normal")
        layer.set_font_size(20)
        layer.move_to(win.current["w"]/2-180,
            current_Y + win.scroll["pm_update"] + 140)
        layer.show_text(str(version)+" "+sufix)
        
        def do():
            os.system("xdg-open "+link.replace("(", "\(").replace(")", "\)"))
        
        UI_elements.roundrect(layer, win, 
            win.current["w"]/2-200,
            110 + current_Y + win.scroll["pm_update"],
            410,
            40,
            10,
            button=do,
            tip=talk.text("update_read_version_notes"),
            fill=False,
            clip=clip)
        layer.stroke()
        
        # Open and Close button. A little side triangle thingy.
        
        if is_open:
            icon = "open"
            expandcall = talk.text("Compress")
        else:
            icon = "closed"
            expandcall = talk.text("Expand")
        
        def do():
            win.update["versions"][version]["open"] = not is_open
            
        UI_elements.roundrect(layer, win, 
            win.current["w"]/2-240,
            110 + current_Y + win.scroll["pm_update"],
            40,
            40,
            10,
            button=do,
            icon=icon,
            tip=expandcall,
            clip=clip)
        
        current_Y = current_Y + 50
        
        if is_open:
            for filename in files:
                UI_color.set(layer, win, "text_normal")
                layer.set_font_size(15)
                layer.move_to(win.current["w"]/2-180,
                    current_Y + win.scroll["pm_update"] + 140)
                layer.show_text(str(filename))
                
                
                def do():
                    gitlink = "https://github.com/JYamihud/VCStudio/commits/main/"
                    os.system("xdg-open "+gitlink+filename)
                
                UI_elements.roundrect(layer, win, 
                    win.current["w"]/2-200,
                    110 + current_Y + win.scroll["pm_update"],
                    410,
                    40,
                    10,
                    button=do,
                    tip=talk.text("update_see_history"),
                    fill=False,
                    clip=clip)
                layer.stroke()
        
                current_Y = current_Y + 50
    
    UI_elements.scroll_area(layer, win, "pm_update", 
        int(win.current["w"]/2-250),
        100,
        500,
        win.current["h"]-260,
        current_Y,
        bar=True,
        mmb=True,
        url="update_layer"
        )
    
    
    return surface
