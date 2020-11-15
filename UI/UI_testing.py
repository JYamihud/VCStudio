# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os

# GTK module ( Graphical interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo

# Own modules
from settings import settings
from settings import talk

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
    
    # Variables I will need tfor animations
    testing_bar = UI_elements.animate("UI_testing_banner", win)
    

    # Testing top banner thingy
    if testing_bar > 0.01:
        layer.set_source_rgba(1,1,1,0.5)
        UI_elements.roundrect(layer,
            5,
            5, 
            (win.current['w']-10)*testing_bar,
            30,
            10)
        layer.fill()
    
    # testing will be drawn only it's activated    
    if win.current["testing"]:
        
        #Animating values
        testing_bar = UI_elements.animate("UI_testing_banner", win, testing_bar, 1, 10, force=True)
        
        
        
        # Current Framerate
        UI_color.set(layer, win, "testing_banner")
        UI_elements.roundrect(layer,
            5,
            5, 
            60,
            30,
            10)
        layer.fill()
        
        UI_color.set(layer, win, "testing_text")
        layer.set_font_size(20)
        layer.move_to(20,27)
        layer.show_text(str(win.FPS))
        
        
    
        # Mouse Visualization thingy
        for n ,button in enumerate(["LMB", "MMB", "RMB"]):            
            
            if win.current[button]:
                UI_color.set(layer, win, button)
                
                #line from click to current mouse position
                layer.move_to(win.current[button][0],
                              win.current[button][1])
                layer.line_to(win.current["mx"],
                              win.current["my"])
                layer.stroke()
                
            else:
                UI_color.set(layer, win, "testing_banner")
            UI_elements.roundrect(layer,
                75 + (35 * n),
                5, 
                30,
                30,
                10)
            layer.fill()
    
        # Keyboard
        UI_color.set(layer, win, "testing_banner")
        UI_elements.roundrect(layer,
            185,
            5, 
            30,
            30,
            10)
        layer.fill()
        
        UI_color.set(layer, win, "testing_text")
        layer.set_font_size(20)
        layer.move_to(195,27)
        layer.show_text(win.current["key_letter"])
        
        for n, key in  enumerate(win.current["keys"]):
            UI_color.set(layer, win, "testing_banner")
            UI_elements.roundrect(layer,
                220 + (80 * n),
                5, 
                75,
                30,
                10)
            layer.fill()
            
            UI_color.set(layer, win, "testing_text")
            layer.set_font_size(20)
            layer.move_to(225 + (80 * n),27)
            layer.show_text(str(key))
    
    else: # if not testing bar
        # Animating back to 0
        testing_bar = UI_elements.animate("UI_testing_banner", win, testing_bar, 0,  10, force=True)
         
    # Switch to activate testing (or diactivate it). Top, Right corner.
    if  win.current['mx'] in range(win.current['w']-35, win.current['w']) \
    and win.current['my'] in range(5, 35) :
        UI_color.set(layer, win, "testing_banner")
        UI_elements.roundrect(layer,
            win.current['w'] - 35,
            5, 
            30,
            30,
            10)
        layer.fill()
        
        # Mouse Click
        if win.current["LMB"] and not win.previous["LMB"]:
            win.current["testing"] = not win.current["testing"]
    
    return surface
