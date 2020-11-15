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

def roundrect(layer, x, y, width, height, r):
    
    # This function draws a rectangle with rounded edges.
    
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
    
    if True:   #toblur:
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
        
