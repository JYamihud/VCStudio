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
    
    UI_color.set(layer, win, "darker_parts")
    UI_elements.roundrect(layer, win,
        50,
        5, 
        win.current["w"] - 55,
        win.current["h"] - 30,
        30)
    
    # Little verion thing in the bottom corner
    UI_color.set(layer, win, "testing_banner")
    layer.set_font_size(15)
    layer.move_to(win.current["w"]-50, win.current["h"] - 7)
    layer.show_text(str(win.version))
    
    
    # Side bar. First 3. New project / Search Projects / Configure Project.
    
    # New Project
    def do():
        print("New Project")
        win.url = "new_project"
    
    UI_elements.roundrect(layer, win,
        5,
        5, 
        40,
        40,
        10,
        do,
        "new_file",
        talk.text("createnewproject_tooltip"),
        url="project_manager")
    
    
    
    # Search for projects
    def do():
        
        win.url = "scan_projects"
        
    UI_elements.roundrect(layer, win,
        5,
        55, 
        40,
        40,
        10,
        do,
        "search_file",
        talk.text("scanforprojects_tooltip"),
        url="project_manager")
    
    
    # Configure
    if win.current["project"] and pm_project.is_legacy(win.current["project"]):
    
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
            talk.text("convertoldproject_tooltip"),
            url="project_manager")
        
    
    # Side bar. Last 3. Internet things / Updater / Settings
    
    # Internet things
    def do():
        win.url = "help_layer"
    
    UI_elements.roundrect(layer, win,
        5,
        win.current["h"]-150, 
        40,
        40,
        10,
        do,
        "question",
        talk.text("pm_internet_tooltip"),
        url="project_manager")
    
    # Update
    def do():
        print("Update")
        os.system("xdg-open https://github.com/JYamihud/VCStudio")
    
    UI_elements.roundrect(layer, win,
        5,
        win.current["h"]-95, 
        40,
        40,
        10,
        do,
        "update",
        talk.text("Update"),
        url="project_manager")
    
    # Internet things
    def do():
        print("Settings")
        os.system("xdg-open "+os.getcwd()+"/settings/settings.data")
    
    UI_elements.roundrect(layer, win,
        5,
        win.current["h"]-45, 
        40,
        40,
        10,
        do,
        "settings",
        talk.text("Settings"),
        url="project_manager")
    
    # Now let's make previews of projects. I think each one will be it's own
    # layer thingy. Just so I could draw things inside them.
    
    # Clipping so it wont draw beyon the frame
    UI_elements.roundrect(layer, win,
        50,
        5, 
        win.current["w"] - 55,
        win.current["h"] - 30,
        30,
        fill=False)
    layer.clip()
    
    # Setting up scroll for Projects
    if "pm_scroll" not in win.current:
        win.current["pm_scroll"] = 0.0
    
    # Setting up tilling
    tileY = 0 
    tileX = 0
    
    if "pm_main" not in win.scroll:
        win.scroll["pm_main"] = 0
    
    for num, project in enumerate(pm_project.get_list()):
        
        
        if tileX > (win.current["w"]-55)-391:
            tileY += 330
            tileX = 0
        
        project_node(layer, win, 60+tileX, 15+tileY+ win.scroll["pm_main"], project)
        
        tileX += 360
    
    UI_elements.scroll_area(layer, win, "pm_main", 
        50,
        5, 
        win.current["w"] - 55,
        win.current["h"] - 30,
        tileY+340,
        bar=True,
        mmb=True,
        url="project_manager"
        )
    
    
    
    return surface
    
def project_node(layer, win, x, y, project):
    
    # This function will draw a project to a given place.
    node_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, win.current['w'],
                                                           win.current['h'])
    node = cairo.Context(node_surface)
    node.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    
    
    # Before we gonna do clip. Let's put here the logic of the node.
    def do():
        print(project)
        win.current["project"] = project
    
    Legacytip = ""
    if pm_project.is_legacy(project): 
        Legacytip = "\nLegacy (Blender-Organizer)"
    node.set_line_width(10)
    UI_elements.roundrect(node, win,
        x-5,
        y-5, 
        350+10,
        320+10,
        20+5,
        button=do,
        fill=False,
        tip=project+Legacytip,
        url="project_manager")
    node.stroke()
    
    # If project is selected
    if win.current["project"] == project and win.previous["project"] == project:
        UI_color.set(node, win, "button_active")
        UI_elements.roundrect(node, win,
            x-5,
            y-5, 
            350+10,
            320+10,
            20+5,
            button=False,
            fill=False
            )
        node.stroke()
        
        def do():
            pm_project.load(project)
            Gtk.main_quit()  # Here I might do some kind a setting later
            
        UI_elements.roundrect(node, win,
            x-5,
            y-5, 
            350+10,
            320+10,
            20+5,
            button=do,
            fill=False,
            url="project_manager"
            )
        
        # Enter keys
        if win.url == "project_manager":
            if 65293 in win.current["keys"] or 65421 in win.current["keys"]:
                do()
                win.current["keys"].remove(65293)
                win.current["keys"].remove(65421)
    
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
    
    
    if os.path.exists(project+"/py_data/banner.png"):
        UI_elements.image(node, win, project+"/py_data/banner.png",
        x,y,350,320)
    else:
        UI_elements.image(node, win, "icon.png",
        x,y,350,320)
   
    # Top Banner thingy
    if pm_project.is_legacy(project): 
        UI_color.set(node, win, "node_badfile")
    else:
        UI_color.set(node, win, "node_blendfile")
    
    node.rectangle(x,y,350,40)
    node.fill()
    
    # Name of the project
    nameonly = project[project.rfind("/")+1:]
    UI_color.set(node, win, "text_normal")
    node.set_font_size(20)
    node.move_to(x+175-len(nameonly)*12/2,y+25)
    node.show_text(nameonly)
    
    # Bottom widget part
    UI_color.set(node, win, "node_background")
    node.rectangle(x,y+250,350,100)
    node.fill()
    
    
    # Drawing the Node on the main layer.
    layer.set_source_surface(node_surface, 0,0)
    layer.paint()
