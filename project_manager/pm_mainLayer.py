# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os

# GTK module ( Graphical interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
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
    
    UI_color.set(layer, win, "darker_parts")
    UI_elements.roundrect(layer, win,
        50,
        5, 
        win.current["w"] - 55,
        win.current["h"] - 10,
        20)
    
    
    
    # Side bar. First 3. New project / Search Projects / Configure Project.
    
    # New Project
    def do():
        print("New Project")
    
    UI_elements.roundrect(layer, win,
        5,
        5, 
        40,
        40,
        10,
        do,
        "new_file",
        talk.text("createnewproject_tooltip"))
    
    
    
    # Search for projects
    def do():
        print("search")
    
    UI_elements.roundrect(layer, win,
        5,
        55, 
        40,
        40,
        10,
        do,
        "search_file",
        talk.text("scanforprojects_tooltip"))
    
    
    # Configure
    def do():
        print("configure")
    
    UI_elements.roundrect(layer, win,
        5,
        110, 
        40,
        40,
        10,
        do,
        "configure_file",
        talk.text("convertoldproject_tooltip"))
    
    
    # Side bar. Last 3. Internet things / Updater / Settings
    
    # Internet things
    def do():
        print("Internet")
    
    UI_elements.roundrect(layer, win,
        5,
        win.current["h"]-150, 
        40,
        40,
        10,
        do,
        "internet",
        talk.text("pm_internet_tooltip"))
    
    # Update
    def do():
        print("Update")
    
    UI_elements.roundrect(layer, win,
        5,
        win.current["h"]-95, 
        40,
        40,
        10,
        do,
        "update",
        talk.text("Update"))
    
    # Internet things
    def do():
        print("Settings")
    
    UI_elements.roundrect(layer, win,
        5,
        win.current["h"]-45, 
        40,
        40,
        10,
        do,
        "settings",
        talk.text("Settings"))
    
    # Now let's make previews of projects. I think each one will be it's own
    # layer thingy. Just so I could draw things inside them.
    
    # Clipping so it wont draw beyon the frame
    UI_elements.roundrect(layer, win,
        50,
        5, 
        win.current["w"] - 55,
        win.current["h"] - 10,
        20,
        fill=False)
    layer.clip()
    
    # Setting up tilling
    tileY = 0
    tileX = 0
    for num, project in enumerate(pm_project.get_list()):
        
        
        if tileX > (win.current["w"]-55)-391:
            tileY += 330
            tileX = 0
        
        project_node(layer, win, 60+tileX, 15+tileY, project)
        
        tileX += 360
    
    return surface
    
def project_node(layer, win, x, y, project):
    
    # This function will draw a project to a given place.
    node_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, win.current['w'],
                                                           win.current['h'])
    node = cairo.Context(node_surface)
    node.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    
    # This next roundrect will both be the backdrop of the node and both will 
    # clip the node content. All folowing graphics will be drawn clipped to the
    # current roundrect.
    
    UI_color.set(node, win, "node_background")
    UI_elements.roundrect(node, win,
        x,
        y, 
        350,
        320,
        20)
        
    # Clip
    UI_elements.roundrect(node, win,
        x,
        y, 
        350,
        320,
        20,
        fill=False)
    node.clip()
    
    # Top Banner thingy
    Legacy = True
    UI_color.set(node, win, "node_badfile")
    
    # If New ( VCStudio ), and not legacy ( Blender-Organizer )
    if os.path.exists(project+"/set"): 
        UI_color.set(node, win, "node_blendfile")
        Legacy = False
    
    node.rectangle(x,y,350,40)
    node.fill()
    
    # Name of the project
    UI_color.set(node, win, "text_normal")
    node.set_font_size(20)
    node.move_to(x+20,y+25)
    node.show_text(project[project.rfind("/")+1:])
    
    # Drawing the Node on the main layer.
    layer.set_source_surface(node_surface, 0,0)
    layer.paint()
