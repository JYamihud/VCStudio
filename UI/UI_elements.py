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

def roundrect(ctx, x, y, width, height, r):
    
    # This function draws a rectangle with rounded edges.
    
    # Making sure that round rectangle will not be smaller then it's roundness
    # Also you could use it as a cirle by putting height and width to 0
    if width < r*2:
        width = r*2
    if height < r*2:
        height = r*2
    
    # actuall drawing
    ctx.move_to(x,y)
    ctx.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    ctx.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
    ctx.arc(x+width-r, y+height-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+height-r, r, math.pi/2, math.pi)
    ctx.close_path()

