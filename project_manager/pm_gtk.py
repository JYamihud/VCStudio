# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os
import datetime

# GTK module ( Graphical interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo

# Own modules
from settings import settings
from settings import talk
from project_manager import pm_project
from project_manager import pm_mainLayer

# UI modules
from UI import UI_testing
from UI import UI_color
from UI import UI_elements

# OK let's make a window
def run():
    # In the Blender-Organizer I was putting the version into the title. Not cool.
    # Because if you would snap it to the sidebar in Ubuntu. On mouse over it would
    # show the first ever version. So there will be a better way to see version.
    # I think let's do that like in Blender. Drawn with in the window somewhere.

    # Setting up the window
    win = Gtk.Window()
    win.maximize()
    win.connect("destroy", Gtk.main_quit)
    win.set_title("VCStudio : "+talk.text("project-manager"))
    win.set_default_icon_from_file("tinyicon.png")
    
    # Setting up the events ( mouse and keyboard handling )
    win.connect("button-press-event", mouse_button_press, win)
    win.connect("button-release-event", mouse_button_release, win)
    win.connect("key-press-event", key_press, win)
    win.connect("key-release-event", key_release, win)
    

    
    # Setting up the global variables. (kinda)
    win.animations = {}
    win.previous   = {}
    win.current    = {}
    win.images     = {}
    win.FPS        = 0
    
    # Cashed tables
    win.color    = UI_color.get_table()
    win.settings = settings.load_all()
    
    # Default values
    win.current["frame"]   = 0
    win.current["testing"] = False
    win.current["LMB"]     = False
    win.current["MMB"]     = False
    win.current["RMB"]     = False
    win.current["keys"]    = []
    win.current["key_letter"] = ""
    win.sFPS = datetime.datetime.now()
    
    # Setting the drawable
    pmdraw = Gtk.DrawingArea()
    pmdraw.set_size_request(815, 500)
    win.add(pmdraw)
    pmdraw.connect("draw", pmdrawing, win)
    pmdraw.connect("scroll-event", scroll_event, win)
    
    #run
    win.show_all()
    Gtk.main()


def pmdrawing(pmdrawing, main_layer, win):
    
    # This function draws the actuall image. I'm doing full frames redraws. It's
    # a bit simpler then making some kind of dynamic draw call system that might
    # be used in such an application. But to hell with it. I did the same on the
    # Blender-Organizer altho with way less cairo. And it works well enought.
    
    # FPS counter
    win.fFPS = datetime.datetime.now()
    win.tFPS = win.fFPS - win.sFPS
    if win.current["frame"] % 10 == 0:
        win.FPS = int ( 1.0 / ( win.tFPS.microseconds /1000000))
    
    win.sFPS = datetime.datetime.now()
    
    # Current frame (for animations and things like this)
    win.current["frame"] += 1    
    
    # Getting data about the frame
    win.current['mx'] = win.get_pointer()[0]
    win.current['my'] = win.get_pointer()[1]
    win.current['w']  = win.get_size()[0]
    win.current['h']  = win.get_size()[1]
    
    
    #Background color
    UI_color.set(main_layer, win, "background")
    main_layer.rectangle(
    0,
    0,
    win.current['w'],
    win.current['h'])
    main_layer.fill()
    
    # Tooltips and other junk has to be defined here. And then drawn later to 
    # the screen. So here we get a special layer. That will be drawn to during
    # the time of drawing. And later composeted over everything. 
    
    win.tooltip_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, win.current['w'],
                                                                  win.current['h'])
    win.tooltip = cairo.Context(win.tooltip_surface)
    win.tooltip.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    
    
    # Layers. Order of them matter
    Layers = []
    Layers.append(pm_mainLayer.layer(win))
    Layers.append(UI_testing.layer(win))
    Layers.append(win.tooltip_surface)
    
    # Combining layers
    for layer in Layers:
        main_layer.set_source_surface(layer, 0 , 0)
        main_layer.paint()
    
    
    # Saving data about this frame for the next one. A bit hard to get WTF am I
    # doing here. Basically trying to avoid current and previous data to be links
    # of the same data.
    
    win.previous = {}
    for i in win.current:
        if type(win.current[i]) == list or type(win.current[i]) is dict:
            win.previous[i] = win.current[i].copy()
        else:
            win.previous[i] = win.current[i]
    
    
    # Refreshing the frame automatically
    pmdrawing.queue_draw()
    

# This program will have things like mouse and keyboard input. And this setup
# Will be done in both PM and the actuall Project window. ( Also in the render
# Window. Basically all separate windows will have to have this setup separatelly.

# Mouse
def mouse_button_press(widget, event, win):

    # This function marks activation of the button. Not it's deactivation.

    # I'm going to attempt something quite disturbing. Basically I want to save
    # the state of the mouse as the press begun untill it's released. And I'm 
    # going to do in a slightly weird way. Because I'm bored I guess. The prob-
    # lem is that it will require to check whether the data even exists in the
    # first place. If x. Before parsing it. Because it might be False.
    
    for i, button in enumerate(["LMB", "MMB", "RMB"]):
        if i+1 == int(event.get_button()[1]):
            win.current[button] = [event.x, event.y]
            
    # If you folowed the code. By checking for example if win.current["LMB"]
    # You can know if it's even pressed to begin with. Because if it's not
    # It's False.
    
def mouse_button_release(widget, event, win):
    
    # This function reverses the effects of the mouse_button_press() function.
    
    for i, button in enumerate(["LMB", "MMB", "RMB"]):
        if i+1 == int(event.get_button()[1]):
            win.current[button] = False

# I guess it's time to make something similar for the keyboard keys as well.
# I'm going to reuse the old system from the Blender-Organizer. Just a list of
# pressed keys. Maybe as well a strting thingy. Because I want to type in this
# app. 

def key_press(widget, event, win):
    if event.keyval not in win.current["keys"]:
        win.current["keys"].append(event.keyval)
        win.current["key_letter"] = event.string
        
def key_release(widget, event, win):
    try:
        win.current["keys"].remove(event.keyval)
    except:
        win.current["keys"] = []
    
# Now I'm going to attempt to make a functional scroll. IDK because it was a 
# very long thing to do.

def scroll_event(widget, event, win):
    print ("Works")
