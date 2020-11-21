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
        win.current["h"]/2-150,
        500,
        300,
        10)
    
    # Title of the operation. Incase the user forgot. 
    UI_elements.text(layer, win, "new_project_title",
        win.current["w"]/2-250,
        win.current["h"]/2-110,
        500,
        30,
        10,
        fill=False,
        centered=True,
        editable=False)
    if "New-Project-Folder" in win.settings: # It might not exist there.
        win.text["new_project_title"]["text"] = talk.text("createnewproject_tooltip")
    
    
    
    # Folder. It's so VCStudio would know WHERE does user want to create the 
    # final project.
    
    def do():
        
        folderchooser = Gtk.FileChooserDialog(talk.text("select_folder"),
                                         None,
                                         Gtk.FileChooserAction.SELECT_FOLDER,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        folderchooser.set_default_response(Gtk.ResponseType.OK)
        response = folderchooser.run()
        if response == Gtk.ResponseType.OK:
            get = folderchooser.get_filename()
            settings.write("New-Project-Folder", get)
            win.settings["New-Project-Folder"] = get       
        folderchooser.destroy()
        
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2-240,
        win.current["h"]/2-30,
        480,
        40,
        10,
        button=do,
        icon="folder",
        tip=talk.text("pm_new_project_folder_tooltip"))
    
    choseF = "Select Folder"
    if "New-Project-Folder" in win.settings:
        choseF = win.settings["New-Project-Folder"]
    UI_elements.text(layer, win, "new_project_folder",
        win.current["w"]/2-190,
        win.current["h"]/2-30,
        430,
        40,
        set_text=choseF,
        fill=False,
        editable=False
        )
    
    
    # Name of the project folder.  Aka Name of the project
    UI_elements.text(layer, win, "new_project_name",
        win.current["w"]/2-240,
        win.current["h"]/2+20,
        480,
        40,
        set_text=talk.text("new_project_name"))
    
    #win.textactive = "new_project_name"
    # Okay and Cancel buttons
    
    def do():
        
        pm_project.new(win.text["new_project_name"]["text"])
        win.url = "project_manager" 
        win.textactive = ""
        win.text["new_project_name"]["text"] = talk.text("new_project_name")
        
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2+170,
        win.current["h"]/2+110,
        40,
        40,
        10,
        button=do,
        icon="ok",
        tip=talk.text("checked"))
    
    def do():
        win.url = "project_manager" 
        win.textactive = ""
        win.text["new_project_name"]["text"] = talk.text("new_project_name")
        
        
    UI_elements.roundrect(layer, win, 
        win.current["w"]/2+210,
        win.current["h"]/2+110,
        40,
        40,
        10,
        button=do,
        icon="cancel",
        tip=talk.text("cancel"))
    
    
    
    return surface
