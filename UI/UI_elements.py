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

# UI
from UI import UI_color

def roundrect(layer, win, x, y, width, height, r, button=False, icon=False, 
              tip="", fill=True):
    
    # This function draws a rectangle with rounded edges.
    
    # A button variable is a calable for the button action. Basically it's a
    # function. Roundrect will act as a button.
    if button:
        if  win.current['mx'] in range(x, x+width) \
        and win.current['my'] in range(y, y+height) :
            do = True
            
            # If holding click
            if win.current["LMB"]:
                UI_color.set(layer, win, "button_clicked")
            else:
                UI_color.set(layer, win, "button_active")
            # If clicked
            if win.previous["LMB"] and not win.current["LMB"]:
                button()
            
            # Button might have a tooltip as well
            if tip:
                tooltip(win, tip)
        
        else:
            do = False
        
        
        
    else:
        do = True
    
    if do:
        # Making sure that round rectangle will not be smaller then it's roundness
        # Also you could use it as a cirle by putting height and width to 0
        if width < r*2:
            width = r*2
        if height < r*2:
            height = r*2
        
        # actuall drawing
        layer.move_to(x,y)
        layer.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
        layer.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
        layer.arc(x+width-r, y+height-r, r, 0, math.pi/2)
        layer.arc(x+r, y+height-r, r, math.pi/2, math.pi)
        layer.close_path()
        if fill:
            layer.fill()
    
    # Icon is a continuation of the button part. Because you need a way to see
    # that that the button is even there to begin with.
    if icon:
        image(layer, win, "settings/themes/"\
        +win.settings["Theme"]+"/icons/"+icon+".png", x, y)
    
def animate(name, win, v1=0, v2=None, time=10, force=False):
    
    # This function will make animating values over time possible. For smooth
    # Transisions and things like this it's going to be very usefull.
    
    # Let's clear mess in case they I'm lazy to make all the things
    if v2 == None:
        v2 = v1
        
    # Set up the animation into the animations. If it's not there yet.
    if name not in win.animations or force:
        win.animations[name] = [
            v1,
            v2,
            time,
            win.current["frame"]
            ]
   
    # Let's get data out of the win.animation[name]
    v1    = win.animations[name][0]
    v2    = win.animations[name][1]
    time  = win.animations[name][2]
    start = win.animations[name][3]
    frame = win.current["frame"]
    
    # If animation is over.
    if start + time < frame:
        return v2
    
    # If v1 and v2 are the same. I'm doing it here. In case the value would be
    # Animated later. So it will create the animation instance.
    if v1 == v2:
        return v2
    
    if v1 < v2:
        vN = v1 + ((v2 - v1)/time*(frame-start))
    else:
        vN = v1 - ((v1 - v2)/time*(frame-start))
    
    return vN    
    
def blur(surface, win, amount):
    
    # This function will blur a given layer by scaling it down and scaling it 
    # back up. It will be doing it only when a given blur setting it active.
    
    # To avoid all kinds of Zero devision problems. And speed up the draw if
    # using animated blur values.
    if amount == 0:
        return surface
    
    # Setting up initial Blur
    if not "Blur" in win.settings:
        settings.write("Blur", True)       # Writing to file
        win.settings = settings.load_all() # Loading file back to RAM
    
    # If to active blur. Will be changed in the graphics settings. 
    if win.settings["Blur"]:
        # scaling down
        surface1 = cairo.ImageSurface(cairo.FORMAT_ARGB32, win.current['w'],
                                                           win.current['h'])
        slacedownlayer = cairo.Context(surface1)
        slacedownlayer.scale(1/amount, 
                             1/amount)
        
        slacedownlayer.set_source_surface(surface, 0 , 0)
        slacedownlayer.paint()
        
        #scaling back up
        surface2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, win.current['w'],
                                                           win.current['h'])
        slaceuplayer = cairo.Context(surface2)
        slaceuplayer.scale(amount, 
                           amount)
        
        slaceuplayer.set_source_surface(surface1, 0 , 0)
        slaceuplayer.paint()
        
        return surface2
    else:
        return surface

def image(layer, win ,path, x, y):
    
    # This module will handle drawing images to the layers. It's not that hard
    # to do in cairo by default. But i'm doing it at every frame. And so it
    # means a system of images should exist to take out the load. Basically
    # it will make sure the images is loaded only ones. And for the next draw
    # calls it will forward the old image.
    
    # If image still not loaded
    if path not in win.images:
        # Loading the image into the cairo.
        try:
            imagesurface = cairo.ImageSurface.create_from_png(path)
        except:
            imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
        
        # Saving it into the win.images
        win.images[path] = imagesurface
    
    #loading it back
    else:
        imagesurface = win.images[path]
    
    # Writting the image to the screen
    layer.set_source_surface(imagesurface, x, y)
    layer.paint()

def tooltip(win, text):
    
    layer = win.tooltip
    
    # This function draws a tooltip helper window. 
    
    # Just in case
    text = str(text)
    
    # Let's get dimantions of the cube first.
    lines = 0
    maxletters = 0
    
    for line in text.split("\n"):
        lines += 1
        
        if len(line) > maxletters:
            maxletters = len(line)
    
    
    # Now when we now the mount of lines and the max lenght of a line. We can
    # start actually drawing something.
    
    # Let's try to make so it's not out of the frame.
    sx = win.current["mx"]
    sy = win.current["my"]
    
    if sx+(maxletters*9)+40 > win.current["w"]:
        sx -= (maxletters*9)+40
    if sy+(lines*20)+10 > win.current["h"]:
        sy -= (lines*20)+10   
    
    # Rectangle
    UI_color.set(layer, win, "node_background")
    roundrect(layer, win,
    sx,
    sy,
    (maxletters*9)+40,
    (lines*20)+10,
    10)
    
    
    # Text it self
    layer.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    layer.set_font_size(15)
    UI_color.set(layer, win, "text_normal")
    
    for num, line in enumerate(text.split("\n")):
        layer.move_to(sx+20,
                      sy+20+(20*num) )
        layer.show_text(line)
