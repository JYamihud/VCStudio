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
    if "pm_settings" not in win.scroll:
        win.scroll["pm_settings"] = 0
    
    current_Y = 0 # The max scroll value
    
    # Preparing lists.
    if "settings_lists" not in win.current:
        
        win.current["settings_lists"] = {}
        win.current["settings_lists"]["languages"] = settings.list_languages()
        win.current["settings_lists"]["languages_open"] = False
    
    
    # Languages
    def do():
        win.current["settings_lists"]["languages_open"] = \
        not win.current["settings_lists"]["languages_open"]
        
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2-240,
        110 + current_Y + win.scroll["pm_settings"],
        450,
        40,
        10,
        button=do,
        icon="font",
        tip=talk.text("change_language"))
    
    UI_color.set(layer, win, "text_normal")
    layer.set_font_size(20)
    layer.move_to(win.current["w"]/2-180,
        current_Y + win.scroll["pm_settings"] + 140)
    layer.show_text(win.settings["Language"])
    
    current_Y += 50
    
    if win.current["settings_lists"]["languages_open"]:
        for lang in win.current["settings_lists"]["languages"]:
            if lang != win.settings["Language"]:
                
                def do():
                    win.settings["Language"] = lang
                    settings.write("Language", lang)
                    win.current["settings_lists"]["languages_open"] = False
                
                UI_elements.roundrect(layer, win, 
                    win.current["w"]/2-200,
                    110 + current_Y + win.scroll["pm_settings"],
                    410,
                    40,
                    10,
                    button=do,
                    icon="font",
                    tip=talk.text("set_language")+lang)
                
                
                UI_color.set(layer, win, "text_normal")
                layer.set_font_size(20)
                layer.move_to(win.current["w"]/2-140,
                    current_Y + win.scroll["pm_settings"] + 140)
                layer.show_text(lang)
                
                current_Y += 50
    
    # BLUR
    
    blur_ok = False            
    if win.settings["Blur"]:
        blur_ok = "ok"
                
    def do():
        win.settings["Blur"] = not win.settings["Blur"]
        settings.write("Blur", win.settings["Blur"])
    
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2-240,
        110 + current_Y + win.scroll["pm_settings"],
        450,
        40,
        10,
        button=do,
        icon=blur_ok,
        tip=talk.text("Blur"))
    
    UI_color.set(layer, win, "text_normal")
    layer.set_font_size(20)
    layer.move_to(win.current["w"]/2-180,
        current_Y + win.scroll["pm_settings"] + 140)
    layer.show_text(talk.text("Blur"))
    
    current_Y += 50
    
    if win.settings["Blur"]:
        ablur_ok = False            
        if win.settings["Auto_De-Blur"]:
            ablur_ok = "ok"
        
        def do():
            win.settings["Auto_De-Blur"] = not win.settings["Auto_De-Blur"]
            settings.write("Auto_De-Blur", win.settings["Auto_De-Blur"])
        
        UI_elements.roundrect(layer, win, 
            win.current["w"]/2-240,
            110 + current_Y + win.scroll["pm_settings"],
            450,
            40,
            10,
            button=do,
            icon=ablur_ok,
            tip=talk.text("Auto_De-Blur"))
        
        UI_color.set(layer, win, "text_normal")
        layer.set_font_size(20)
        layer.move_to(win.current["w"]/2-180,
            current_Y + win.scroll["pm_settings"] + 140)
        layer.show_text(talk.text("Auto_De-Blur"))
    
    
    current_Y += 50
    
    UI_elements.scroll_area(layer, win, "pm_settings", 
        int(win.current["w"]/2-250),
        100,
        500,
        win.current["h"]-260,
        current_Y,
        bar=True,
        mmb=True,
        url="settings_layer"
        )
    
    
    return surface
