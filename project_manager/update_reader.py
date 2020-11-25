# THIS FILE IS A PART OF VCStudio
# PYTHON 3

import os
from subprocess import *


def get_update_info(win):
    
    # In the GTK version you could make updates by downloading new versions of
    # the files from the GIT repository. But it's not an easy thing to set up
    # seamlessly for the user. IK because similar system is already in place
    # for the Blender-Organizer.
    
    # This system will be somewhat simplified in the UI side of things. But a 
    # tiny bit more complex from the underliying system. For example. In the old
    # release there was no notification of the update. 
    
    # So this function here will check for updates. 
    
    # Now I have no idea how to implement update notifications. And whether I 
    # should in the first place. In the old update system I had often made 
    # easy to fix mistakes. But I was relying a little bit on the fact that
    # people don't see immediatly that the update is available. Which I could
    # use to fix all the mistakes I found without calling a whole another 
    # version. Maybe it's a good thing here too.
    
    # I think that since VCStudio Project-Manager is going to be ran as a kind
    # of launcher thingy... People will more often use the VCStudio it self and
    # rearly the launcher. And so, some kind of automatic update check could be
    # done. And no nasty notification. Just a number on the update icon.
    
    # Now to make it work. I need to separate the reading of network to a separate
    # python file. update_request.py . That I gonna run as a subprocess to this
    # file.
    
    # The updating it self will have to be confirmed by the user. For which will
    # need a UI layer. pm_updateLayer.py and a update download file for actually
    # donloading and saving those files. update_download.py
    
    # So let's start already.
    
    
    if "request" not in win.update:
        
        # This is going to open a SUBPROCESS for the getting of the update info
        # I'm doing it like this so there will not be lag.
        win.update["request"] = Popen(['stdbuf', '-o0',  "python3", \
            os.getcwd()+"/project_manager/update_request.py"],\
            stdout=PIPE, universal_newlines=True)
        win.update["versions"] = {}
        win.update["get_files"] = []
        
    elif "END" not in win.update:
        # This going to read lines returned by the process on every frame.
        line = win.update["request"].stdout.readline()[:-1]
        
        
        if line:
            if line.startswith("VERSION "):
                try:
                    now_version = float(line.replace("VERSION ", ""))
                    
                    if "count" not in win.update:
                        win.update["count"] = 0
                    
                    if now_version > win.version:
                        win.update["count"] += 1
                    
                    win.update["now_version"] = now_version
                    
                    if now_version not in win.update["versions"]:
                        win.update["versions"][now_version] = {
                            "open":False,
                            "files":[],
                            "link":"https://github.com/JYamihud/VCStudio"
                            }
                except:
                    raise()
                    pass
                
            elif line.startswith("["):
                try:
                    win.update["versions"][win.update["now_version"]]["link"] = \
                    line[1:-1]
                except:
                    pass
            elif line != "END":
                try:
                    win.update["versions"][win.update["now_version"]]["files"]\
                    .append(line)
                    
                    if win.update["now_version"] > win.version:
                        if line not in win.update["get_files"]:
                            win.update["get_files"].append(line)
                    
                except:
                    pass
        
        # To end the reading non-sense
        if line == "END":
            win.update["END"] = True
        
        
