# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os
import math

# GTK module ( Graphical interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GdkPixbuf
import cairo

# Own modules
from settings import settings
from settings import talk

# UI
from UI import UI_color

def roundrect(layer, win, x, y, width, height, r, button=False, icon=False, 
              tip="", fill=True, url="", clip=False):
    
    # This function draws a rectangle with rounded edges.
    
    # A button variable is a calable for the button action. Basically it's a
    # function. Roundrect will act as a button.
    if button:
        
        #if not current url in the software
        if url and url != win.url:
            return
        
        # If UI testing is on preview. Buttons.
        if win.current["testing"]:
            UI_color.set(layer, win, "testing_banner")
            layer.rectangle(x,y,width,height)
            layer.stroke()
        
        
        if  win.current['mx'] in range(int(x), int(x+width)) \
        and win.current['my'] in range(int(y), int(y+height)) :
            do = True
            
            if clip:
                if  win.current['mx'] in range(int(clip[0]), int(clip[0]+clip[2])) \
                and win.current['my'] in range(int(clip[1]), int(clip[1]+clip[3])) :
                    do = True
                else:
                    do = False
        
        else:
            do = False
        
        
            
        if do:
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
        do = True
    
    if do:
        # Making sure that round rectangle will not be smaller then it's round-
        # ness. Also with width and height zero, it's going to draw a circle.
        
        if width < r*2:
            width = r*2
        if height < r*2:
            height = r*2
        
        # actuall drawing
        layer.move_to(x,y+r)
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
    if amount < 3: # When Blue value was less then 3 it felt sharp but not enough
        return surface # Which caused sense of uneasiness. 
    
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

def image(layer, win ,path, x, y, width=0, height=0, fit="crop"):
    
    # This module will handle drawing images to the layers. It's not that hard
    # to do in cairo by default. But i'm doing it at every frame. And so it
    # means a system of images should exist to take out the load. Basically
    # it will make sure the images is loaded only ones. And for the next draw
    # calls it will forward the old image.
    
    # Attempt of optimization. Keeping in mind the nature of the programm. Basi-
    # cally I will not load image unless x and y are in frame. Kind a ugly. I
    # know. But I don't want to even bother checking the resolution of the image
    # if it's not in a frame. Roughly speaking. Will see maybe I will make do
    # something to make it better.
    
    if int(x) not in range(int(0-width ), int(win.current["w"])) or \
       int(y) not in range(int(0-height), int(win.current["h"])) :
        return
    
    # If you ran this software you probably noticed that images are loading
    # dynamically. I did it using this following crazy algorythm borowed from
    # the old organizer. Basically for each image I see it's any image is loading
    # at the moment. If yes, wait. If not loading. Meaning it can take the turn
    # I create a thread using GLib. Because I'm lazy. Which is loading the image.
    # Basically the UI keeps working before all images are loaded. 
    
    if path not in win.images or win.images[path] == "LOADING-IMAGE": 
        
        win.images[path] = "LOADING-IMAGE"
        
        if not win.imageload:
            win.imageload = True
            def loadimage(layer, win ,path, x, y, width, height, fit):
                
                # Loading the image into the cairo.
                try:
                    # It could be not PNG
                    try:
                        loadimage = cairo.ImageSurface.create_from_png(path)
                    except:
                        # If it's not png it's gonna take few steps
                        
                        # First we need to make a pixbuf. 
                        load1 = GdkPixbuf.Pixbuf.new_from_file(path)
                        Px = load1.get_width()
                        Py = load1.get_height()
                        
                        # Then to convert the pixbuf to a cairo surface
                        loadimage = cairo.ImageSurface(cairo.FORMAT_ARGB32, Px, Py)
                        imagedraw = cairo.Context(loadimage)
                        Gdk.cairo_set_source_pixbuf( imagedraw, load1, 0, 0)
                        imagedraw.paint()
                        
                    # If I want to resize the image for an icon or something. There is            
                    # gonna be the folowing algorythm.
                    
                    if width or height:
                        
                        dx = 0
                        dy = 0
                        
                        
                        imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
                        imagedraw = cairo.Context(imagesurface)
                        
                        # Crop effect. Really hard on my brains.
                        
                        if fit == 'crop':
                            if height > loadimage.get_height()\
                            or width  > loadimage.get_width():
                                
                                dx = (width/2) -(loadimage.get_width() /2)
                                dy = (height/2)-(loadimage.get_height()/2)
                                
                            else:
                                factor = 1
                                if (loadimage.get_height()*(width/loadimage.get_width()))\
                                    < height:
                                    factor = height / loadimage.get_height()
                                else:
                                    factor = width / loadimage.get_width()
                                #factor = 0.1
                                imagedraw.scale(factor, factor)    
                                dx = (width/2)/factor -(loadimage.get_width() /2)
                                dy = (height/2)/factor -(loadimage.get_height()/2)
                                
                                
                                
                        imagedraw.set_source_surface(loadimage, dx, dy)
                        imagedraw.paint()            
                                
                        
                    else:
                        imagesurface = loadimage
                except Exception as e:
                    print(e)
                    imagesurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
                
                # Saving it into the win.images
                win.images[path] = imagesurface
                win.imageload = False
            
            GLib.timeout_add(1, loadimage, layer, win ,path, x, y, width, height, fit)
            
    #loading it back
    else:
        if  win.images[path] != "LOADING-IMAGE":
            imagesurface = win.images[path]
            
            # Writting the image to the screen
            layer.set_source_surface(imagesurface, x, y)
            layer.paint()
            
            # And if testing
            
            if win.current["testing"]:
                UI_color.set(layer, win, "testing_image")
                layer.rectangle(x,y,imagesurface.get_width(),imagesurface.get_height())
                layer.stroke()

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
        sx = win.current["w"] - ((maxletters*9)+40)
    if sy+(lines*20)+10 > win.current["h"]:
        sy = win.current["h"] - ((lines*20)+10)   
    
    # Rectangle
    UI_color.set(layer, win, "node_background")
    roundrect(layer, win,
    sx,
    sy,
    (maxletters*9)+40,
    (lines*20)+10,
    10)
    
    
    # Text it self
    layer.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL,
                                        cairo.FONT_WEIGHT_NORMAL)
    layer.set_font_size(15)
    UI_color.set(layer, win, "text_normal")
    
    for num, line in enumerate(text.split("\n")):
        layer.move_to(sx+20,
                      sy+20+(20*num) )
        layer.show_text(line)
        
def scroll_area(layer, win, name, x, y, width, height, maxlength, 
                           bar=False,sideways=False, mmb=False, mmb_only=False,
                           url=""):
    
    # This function going to handle all the scrolling windows. Making it so it's
    # relativelly simple to set up big widgets with in small areas. 
    # It will handle only the value of the scroll stored in win.scroll[name]
    
    # First let's set one up if it's not setup
    if name not in win.scroll:
        win.scroll[name] = 0
        return
    
    # Getting scroll amount based on all kinds of settings. AT THIS MOMENT
    # IT'S IN AN ALPHA BECAUSE I'M LAZY. I GONNA IMPLEMENT THING AS I NEED THEM
    # Or you can do that. IDK...
    
    amount = 0.0
    if  win.current['mx'] in range(x, x+width) \
    and win.current['my'] in range(y, y+height) :
        if not mmb_only:
            if not sideways:
                amount = win.current["scroll"][1]*50
            else:
                amount = win.current["scroll"][0]*50
        
        if mmb_only:
            mmb = True
        
        # Middle mouse button scroll, or using a graphical tablet.
        if mmb:
            if win.current["MMB"]:
                amount = 0 - ( win.current["my"] - win.previous["my"] )
    
    # I guess I need to separate the logic into a separate minifunction.
    # I will use later for the scroll bar thingy. So not to rewrite the code
    # Here is a function thingy.
    
    def logic():
        if url and url != win.url:
            return
        # Scroll logic
        win.scroll[name] -= amount
        
        # If too low  
        if win.scroll[name] < (1-maxlength+height):
            win.scroll[name] = (1-maxlength+height)
        # If too high
        if win.scroll[name] > 0:
            win.scroll[name] = 0    
    logic()
    # Not BAR. Which is going to be drawn at a side of what ever content there
    # Basically a scrollbar. But implemented from scratch. Because I'm crazy.
    # and have nothing better to do now.
    
    if bar:
        
        # For now I'm going to implement only vertical bar. I gonna implement
        # the horisontal one when the time comes.
        
        if not sideways:
            
            # Fist let's make some math in front. Because things like this
            # require ton of maths. And it's good to have some predone.
            
            tobreak = False # Also if we can abort the operation early with it.
            fraction = height / maxlength # Similar to progress bar for now
            if fraction > 1:
                tobreak = True
            
            # To break parameter basically says. To draw it the bar only when 
            # it's actully needed. When content aka maxlength is bigger then
            # our viewport.
            
            if not tobreak:
                
                # Now the offset value. That will move our progress bar with 
                # the scroll value.
                
                offset = (height-60)*( (1-win.scroll[name])  / maxlength )        
                
                # Background bar
                
                UI_color.set(layer, win, "background")
                roundrect(layer, win,
                (x+width)-20,
                y+30,
                10,
                height-60,
                5
                )
                
                # Active bar
                
                UI_color.set(layer, win, "button_active")
                
                # Let's save a little bit more math because it's going to be
                # vild. And I love it.
                
                Lx  = (x+width)-20
                LSx = 10
                Ly  = y+30+offset
                LSy = (height-60)*fraction
                
                # Mouse over thingy. To make the bat a tiny bit brighter. 
                # indicating to the user that it's now could be used.
                
                if  win.current['mx'] in range(int(Lx), int(Lx+LSx)) \
                and win.current['my'] in range(int(Ly), int(Lx+LSy)) :
                    UI_color.set(layer, win, "button_clicked")
                
                # Now separatelly we gonna check for if the mouse pressed. 
                # Remember if it's not pressed it's False. It's written in one
                # of the files. Basically I want to be able to move the mouse
                # outside the bar while moving. And so it won't cancel the motion.
                
                # It seems like I did something wrong. Anyways it works.
                
                if win.current["LMB"]:
                    if  int(win.current['LMB'][0]) in range(int(Lx), int(Lx+LSx)) \
                    and int(win.current['LMB'][1]) in range(int(Ly), int(Lx+(height-60))) :
                        
                        UI_color.set(layer, win, "button_clicked")
                        
                        # A bit more math to set the value back.
                        amount = ( win.current["my"] - win.previous["my"] ) / \
                                   (height-60) * maxlength
                        logic() # Yeah. Look a few lines back.
                
                # And only after all of this nonsense we can draw the cube. Or
                # should I say roundrect? A button? Aaaaaa.... 
                
                roundrect(layer, win,
                Lx,
                Ly,
                LSx,
                LSy,
                5
                )
                

def text(outlayer, win, name, x, y, width, height, set_text="", parse=False, fill=True,
        editable=True, multiline=False , linebreak=False, centered=False):
    
    # This function will handle all the text writting in the software.
    # I'm not sure about how parsing going to work for script files later. 
    # But if it's currently works, means that I already implemented it into 
    # the program. 
    
    # Making the layer
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    layer = cairo.Context(surface)
    layer.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    layer.set_font_size(20)
    
    # Some challenges that it will have is how to correctly store data about
    # the text in the system. I think we can use the win.text variable to store
    # directories of the data.
    
    if name not in win.text:
        
        # I need to get something done before I can pu scroll in.
        scrollname = name
        while scrollname in win.scroll:
            scrollname = scrollname+"_text"
        
        win.text[name] = {
            "text"  :set_text,  # Actuall text you are editing.
            "cursor":[len(str(set_text)),len(str(set_text))], # Cursor
            "insert":False, # Whether the insert mode is on
            "scroll":scrollname # If multiline. The pointer for the scroll value.
            }
    
    # Background
    if fill:
        UI_color.set(layer, win, "darker_parts")
        roundrect(layer, win, 
            0,
            0,
            width,
            height,
            10)
        layer.fill()
    
    # Now after filling it up. I want to clip everything. SO no text will get
    # out of a given area. 
    roundrect(layer, win, 
        0,
        0,
        width,
        height,
        10, 
        fill=False)
    layer.clip()
    
    # Now I want to give a preview of the text it self. BUT. I need to be sure 
    # that if the text longer then a given width and there is no multiline or a
    # linebreak. Then it scrolls sideways to the cursor. 
    
    # Automatic scroll system: Based on the position of the cursor.
    offsetX = 0
    cursor2location = win.text[name]["cursor"][1]*12 + offsetX
    while cursor2location > width - 50:
        offsetX -= 1
        cursor2location = win.text[name]["cursor"][1]*12 + offsetX
        
    
    # Text selection. AKA cursor
    # So here we draw the cursor
    if editable:
        UI_color.set(layer, win, "node_blendfile")
        if win.text[name]["cursor"][0] == win.text[name]["cursor"][1]:
            layer.rectangle(
                win.text[name]["cursor"][0]*12+5 +offsetX,
                5,
                (win.text[name]["cursor"][1]*12)-(win.text[name]["cursor"][0]*12)+2,
                30
                )
        else:
            roundrect(layer, win, 
                win.text[name]["cursor"][0]*12+5 +offsetX,
                5,
                (win.text[name]["cursor"][1]*12)-(win.text[name]["cursor"][0]*12)+2,
                30,
                5,
                fill=False
                )
        if win.textactive == name:
            layer.fill()
        else:
            layer.stroke()
    
    
    # Making sure that cursor is correct. Because a lot of bugs are happening
    # with it and it's not cool.
    
    # Mouse select
    if win.current["LMB"]:
        if int(win.current["mx"]) in range(int(x), int(x+width))\
        and int(win.current["my"]) in range(int(y), int(y+height)):
            win.text[name]["cursor"][0] = int((win.current["LMB"][0]-x-offsetX)/12)
            win.text[name]["cursor"][1] = int((win.current["mx"]-x-offsetX)/12)
            
    # If second part of selection ends up bigger then the first. Reverse them.
    if win.text[name]["cursor"][0] > win.text[name]["cursor"][1]:
        win.text[name]["cursor"] = [
            win.text[name]["cursor"][1],
            win.text[name]["cursor"][0]]
    
    # If any part ends up beyond the text. Clip them in.
    if win.text[name]["cursor"][0] < 0:
        win.text[name]["cursor"][0] = 0
    if win.text[name]["cursor"][1] < 0:
        win.text[name]["cursor"][1] = 0
    if win.text[name]["cursor"][0] > len(str(win.text[name]["text"])):
        win.text[name]["cursor"][0] = len(str(win.text[name]["text"]))
    if win.text[name]["cursor"][1] > len(str(win.text[name]["text"])):
        win.text[name]["cursor"][1] = len(str(win.text[name]["text"]))
    
    
    
    # Drawing the text
    
    UI_color.set(layer, win, "text_normal")
    layer.move_to(5+offsetX, height/2+5)
    if centered:
        layer.move_to(width/2-len(str(win.text[name]["text"]))*12/2, height/2+5)
    layer.show_text(str(win.text[name]["text"]))
    
    # Editing the text
    if win.current["keys"] and editable and name == win.textactive:
        # Let's filter the input first. 
        # For example
        if not multiline: #Removing enter key press
            if 65293 in win.current["keys"] or 65421 in win.current["keys"]:
                win.current["key_letter"] = ""
        
        prevlen = len(win.text[name]["text"])
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        regularclean = True
        ORD = 0
        try:
            ORD = ord(win.current["key_letter"])
        except:
            pass
        backremove = False # Whether to make selection go to 0 width thing
        #print(ORD, win.text[name]["cursor"][0])
        
        
        # Backspace
        if 65288 in win.current["keys"]:
            if win.text[name]["cursor"][0] != 0 and win.text[name]["cursor"][0]\
                                           == win.text[name]["cursor"][1]:
                
                win.text[name]["text"] = win.text[name]["text"]\
                [:win.text[name]["cursor"][0]-1]+\
                 win.text[name]["text"]\
                [win.text[name]["cursor"][1]:]
                
            elif win.text[name]["cursor"][1] != 0 and win.text[name]["cursor"][0]\
                                           != win.text[name]["cursor"][1]:
                                           
                win.text[name]["text"] = win.text[name]["text"]\
                [:win.text[name]["cursor"][0]]+\
                 win.text[name]["text"]\
                [win.text[name]["cursor"][1]:]
                backremove = True
            
        # Ctrl - C
        elif ORD == 3:
            
            cliptext = str(clipboard.wait_for_text())
            
            clipboard.set_text( win.text[name]["text"]\
            [win.text[name]["cursor"][0]:win.text[name]["cursor"][1]], -1)
        
        # Ctrl - V
        elif ORD == 22:
            
            cliptext = str(clipboard.wait_for_text())
            
            win.text[name]["text"] = win.text[name]["text"]\
            [:win.text[name]["cursor"][0]]\
             + cliptext +\
            win.text[name]["text"]\
            [win.text[name]["cursor"][1]:]
            win.text[name]["cursor"][0] = win.text[name]["cursor"][1]
        
        # Ctrl - A
        elif ORD == 1:
            win.text[name]["cursor"][0] = 0
            win.text[name]["cursor"][1] = len(win.text[name]["text"])
        
        # To clear up the Controll
        elif 65507 in win.current["keys"]:
            pass
        
        # Shift
        elif 65506 in win.current["keys"]:
            # Right
            if 65363 in win.current["keys"]:
                win.text[name]["cursor"][1] = win.text[name]["cursor"][1] + 1
                #win.current["keys"].remove(65363)
            
            # Left
            elif 65361 in win.current["keys"]:
                if win.text[name]["cursor"][1] > win.text[name]["cursor"][0]:
                    win.text[name]["cursor"][1] = win.text[name]["cursor"][1] - 1
                #win.current["keys"].remove(65361)
                
        # Right button
        elif 65363 in win.current["keys"]:
            win.text[name]["cursor"][0] = win.text[name]["cursor"][0] + 1
            win.text[name]["cursor"][1] = win.text[name]["cursor"][0]
            win.current["keys"].remove(65363)
        
        # Left button
        elif 65361 in win.current["keys"]:
            win.text[name]["cursor"][0] = win.text[name]["cursor"][0] - 1
            win.text[name]["cursor"][1] = win.text[name]["cursor"][0]
            win.current["keys"].remove(65361)
        
        # Escape
        elif 65307 in win.current["keys"]:
            win.textactive = ""
            win.current["keys"].remove(65307)
            
        else:
            win.text[name]["text"] = win.text[name]["text"]\
            [:win.text[name]["cursor"][0]]\
             + win.current["key_letter"]+\
            win.text[name]["text"]\
            [win.text[name]["cursor"][1]:]
            
               
        # Auto moving the cursor    
        nowlen = len(win.text[name]["text"])
        if win.text[name]["cursor"][0] == win.text[name]["cursor"][1]:
            win.text[name]["cursor"][0] = win.text[name]["cursor"][0] + (nowlen - prevlen)
            win.text[name]["cursor"][1] = win.text[name]["cursor"][0]
        
        elif backremove:
            win.text[name]["cursor"][1] = win.text[name]["cursor"][0]
        
        
        if nowlen != prevlen and regularclean:
            # Deleting all the keys from the keys. So yeah.
            win.current["keys"] = [] 
            
    
    
    
    # Outputing to the outlayer. 
    outlayer.set_source_surface(surface, x, y)
    outlayer.paint() 
    
    # Button if editable.
    if editable:
        def do():
            win.textactive = name
        roundrect(outlayer, win, 
            x,
            y,
            width,
            height,
            10, 
            fill=False,
            button=do)
        outlayer.stroke()
    
    if win.textactive == name:
        UI_color.set(outlayer, win, "button_active")
        roundrect(outlayer, win, 
            x,
            y,
            width,
            height,
            10, 
            fill=False)
        outlayer.stroke()

