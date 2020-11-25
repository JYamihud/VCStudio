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
    
    # So it's going to be like a little window in the center of the VCStudio
    # with a simple UI. Probably like 2 things. Folder and a projectname.
    
    UI_color.set(layer, win, "node_background")
    UI_elements.roundrect(layer, win, 
        100,
        100,
        win.current["w"]-200,
        win.current["h"]-200,
        10)
    
    # Exit button
    def do():
        win.url = "project_manager" 
        win.textactive = ""
        
        
    UI_elements.roundrect(layer, win, 
        win.current["w"]-140,
        win.current["h"]-140,
        40,
        40,
        10,
        button=do,
        icon="cancel",
        tip=talk.text("cancel"))
    
    # Clipping everything
    UI_elements.roundrect(layer, win, 
        100,
        110,
        win.current["w"]-200,
        win.current["h"]-260,
        10,
        fill=False)
    layer.clip()
    
    # Setting up the scroll
    if "pm_help" not in win.scroll:
        win.scroll["pm_help"] = 0
    
    current_Y = 1 # The max scroll value
    
    # VCStudio icon. 
    UI_elements.image(layer, win, "tinyicon.png", win.current["w"]/2-205, 
        current_Y+win.scroll["pm_help"]+120 )
    
    UI_color.set(layer, win, "text_normal")
    layer.move_to(win.current["w"]/2-205+148, current_Y+win.scroll["pm_help"]+200)
    layer.set_font_size(50)
    layer.show_text("VCStudio")
    
    # Version
    layer.move_to(win.current["w"]/2-205+148, current_Y+win.scroll["pm_help"]+230)
    layer.set_font_size(20)
    layer.show_text(str(win.version))
    
    current_Y = current_Y+200
    
    # Here I want to put my own credit. And credits of anybody else who will
    # maybe help in future. For now my own credit.
    
    UI_elements.image(layer, win, "project_manager/help_images/Blender_Dumbass_Avatar.png", 140, 
        current_Y+win.scroll["pm_help"]+120 )
    
    UI_color.set(layer, win, "text_normal")
    layer.move_to(280, current_Y+win.scroll["pm_help"]+150)
    layer.set_font_size(20)
    layer.show_text(talk.text("Developer")+":")
    
    layer.move_to(300, current_Y+win.scroll["pm_help"]+190)
    layer.set_font_size(30)
    layer.show_text("J.Y.Amihud")
    
    layer.move_to(280, current_Y+win.scroll["pm_help"]+230)
    layer.set_font_size(25)
    layer.show_text("(Blender Dumbass)")
    
    # Links to my accounts
    
    # Originally I wanted YouTube to be on the list as well. As you may know
    # I have a little YouTube channel called "Blender Dumbass". But I dislike
    # Youtube. And I don't want to promote it. 
    
    # I'm concidering to remove Patreon and Twitter as well. Let me thing about
    # it.
    
    
    links = {
    "Devtalk":"https://devtalk.blender.org/u/blenderdumbass",
    "GitHub":"https://github.com/JYamihud",
    "Telegram 1":"https://t.me/blenderorganizer",
    "Telegram 2":"https://t.me/blenderdumbasschat",
    "Telegram 3":"https://t.me/moriasrace",
    "Patreon":"https://www.patreon.com/blenderdumbass",
    "Twitter":"https://twitter.com/blenderdumbass",
    "Bl-chat":"https://blender.chat/channel/blenderorganizer_vcstudio",
    "LBRY":"https://lbry.tv/$/invite/@BlenderDumbass:c",
    "Music":"https://open.lbry.com/@J.Y.AmihudMusic:c?r=GLhXoQ3zcpvm6rzd9Z6dAyasTpmk1FUY",
    "Movies":"https://open.lbry.com/@VCS:7?r=GLhXoQ3zcpvm6rzd9Z6dAyasTpmk1FUY"
    }
    
    tileY = 50
    tileX = 0
    for link in links:
        
        if tileY < 130:
            posX = 450 + 100
        else:
            posX = 128
        
        def do():
            os.system("xdg-open "+links[link])
        UI_elements.roundrect(layer, win, 
            tileX+posX,
            current_Y+100+tileY+win.scroll["pm_help"],
            170,
            40,
            10,
            button=do,
            icon="internet",
            tip=links[link],
            clip=[
                100,
                110,
                win.current["w"]-200,
                win.current["h"]-260,
                ])
        
        UI_color.set(layer, win, "text_normal")
        layer.move_to(tileX+posX+50, current_Y+win.scroll["pm_help"]+100+tileY+30)
        layer.set_font_size(20)
        layer.show_text(link)
            
        tileX += 170
        if tileX+posX > win.current["w"]-300:
            tileX = 0
            tileY += 50
    
    if tileY > 130:
        current_Y += tileY
    else:
        current_Y += 130
    
    current_Y = current_Y+200
    
    movies = {
        "I'm Not Even Human":[
            "2018/05/01",
            "Blender-Organizer 1.0 - 3.9",
            "https://open.lbry.com/@VCS:7/Imnotevenhumanshortfilm:3?r=GLhXoQ3zcpvm6rzd9Z6dAyasTpmk1FUY",
            "project_manager/help_images/Im_Not_Even_Human_Poster.png"
            ],
        "The Package, The Car & The Time Is Running Out":[
            "2018/11/06",
            "Blender-Organizer 4.0 - 4.17",
            "https://open.lbry.com/@VCS:7/ThePackageTheCarAndTheTimeIsRunningOut:3?r=GLhXoQ3zcpvm6rzd9Z6dAyasTpmk1FUY",
            "project_manager/help_images/The_Package_The_Car_And_Time_Is_Running_Out_Poster.png"
            ],
        "Moria's Race":[
            talk.text("In_Production"),
            "Blender-Organizer 4.18 - VCStudio "+str(win.version),
            "https://t.me/moriasrace",
            "project_manager/help_images/Morias_Race_Poster.png"
            ]
        }
     
    UI_color.set(layer, win, "text_normal")
    layer.move_to(120, current_Y+win.scroll["pm_help"])
    layer.set_font_size(20)
    layer.show_text(talk.text("help_movies_done_title"))
    
    current_Y = current_Y+20
    
    tileX = 120
    for movie in movies:
        UI_elements.image(layer, win, movies[movie][3], tileX, 
        current_Y+win.scroll["pm_help"] , height=300, width=226)
        
        def do():
            os.system("xdg-open "+movies[movie][2])
        UI_elements.roundrect(layer, win, 
            tileX,
            current_Y+win.scroll["pm_help"],
            226,
            300,
            10,
            button=do,
            fill=False,
            tip=movie+"\n"+movies[movie][0]+"\n"+movies[movie][1],
            clip=[
                100,
                110,
                win.current["w"]-200,
                win.current["h"]-260,
                ])
        layer.stroke()
        
        tileX += 300
        if tileX > win.current["w"]-300:
            tileX = 120
            current_Y = current_Y+350
            
    
    current_Y = current_Y+400
    
    # Tutorials about VCStudio.
    UI_color.set(layer, win, "text_normal")
    layer.move_to(120, current_Y+win.scroll["pm_help"])
    layer.set_font_size(20)
    layer.show_text(talk.text("help_tutorial_title"))
    
    current_Y = current_Y+20
    
    tutorials = [
        [talk.text("tutorial_legacy_analitycs"), "https://open.lbry.com/@blender-organizer:5/BlenderOrganizerAnalyticsTutorial4.87:6?r=GLhXoQ3zcpvm6rzd9Z6dAyasTpmk1FUY"],
        [talk.text("tutorial_legacy_storyeditor"), "https://open.lbry.com/@blender-organizer:5/BlenderOrganizerStoryEditorTutorialv4.87:0?r=GLhXoQ3zcpvm6rzd9Z6dAyasTpmk1FUY"],
        [talk.text("tutorial_legacy_assets"), "https://open.lbry.com/@blender-organizer:5/BlenderOrganizerAssetsTutorialv4.87:e?r=GLhXoQ3zcpvm6rzd9Z6dAyasTpmk1FUY"]
        ]
    
    for tutorial in tutorials:
        def do():
            os.system("xdg-open "+tutorial[1])
        UI_elements.roundrect(layer, win, 
            110,
            current_Y+win.scroll["pm_help"],
            win.current["w"]-250,
            40,
            10,
            button=do,
            icon="video",
            tip=talk.text("ClickToWatch"),
            clip=[
                100,
                110,
                win.current["w"]-200,
                win.current["h"]-260,
                ])
            
        UI_color.set(layer, win, "text_normal")
        layer.move_to(160, current_Y+win.scroll["pm_help"]+25)
        layer.set_font_size(20)
        layer.show_text(tutorial[0])
        
        current_Y = current_Y+50
    
    current_Y = current_Y+138
    current_Y = current_Y+138
    
    UI_elements.scroll_area(layer, win, "pm_help", 
        100,
        100, 
        win.current["w"] - 200,
        win.current["h"] - 250,
        current_Y,
        bar=True,
        mmb=True,
        url="help_layer"
        )
    
    
    return surface
