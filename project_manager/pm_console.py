# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os
w, h = os.get_terminal_size() 

from settings import settings
from settings import talk
from project_manager import pm_project


# COMPLITTER
import readline

commands1 = [
"help",#          - help dialogue.
"set_language",#  - changes language settings.
"projects_list",# - see projects list.
"set_folder",#    - set a folder where a new project is created.
"new_project",#   - creates a new project.
"project",#       - launch a given project.
"scan",#          - scans systems for VCStudio or Blender-Organizer projects.
"convert",#       - convert Blender-Organizer project to VCStudio project. (Please have a back up when using this one.)
"exit"# 
]
commands = commands1.copy()

def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

try:
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
except:
    print("NO TABS, SORRY!")

def cls():
    #cleaning the terminal
    os.system("clear")
    
def run():
    
    cls()
    
    
    
    print("\033[1;33m\n   VCStudio - Console \n")
    
    print("\033[1;32m"+talk.text("PMConsoleExplanation")+"\n")
    
    
    while True:
        
        # making sure Tab is doing autocomlete to the right functions
        global commands
        commands = commands1.copy()
        
        command = input("\033[1;35m : \033[1;m")
        
        ##############
        
        if command == "exit":
            cls()
            exit()
        
        ##############
        
        elif command == "help":
            
            print("\033[1;32m"+talk.text("pm_console_help")+"\n")
        
        ##############
        
        elif command == "set_language":
            # Getting list of available languages
            
            commands = []
            for lang in settings.list_languages():    
                print("\033[1;35m "+lang)
                commands.append(lang)
            
            
            # special input for languages
            nlang = input("\033[1;33m : ")
            
            if nlang in settings.list_languages():
                settings.write("Language",nlang)
                print("\033[1;32m"+talk.text("checked"))
            
            else:
                print("\033[1;31m"+talk.text("failed"))
        
        ##############
        
        
        elif command == "set_folder":
            if settings.read("New-Project-Folder"): 
                print("\033[1;35m"+talk.text("Current")+\
                " : "+settings.read("New-Project-Folder"))
            
            nfol = input("\033[1;33m : ")
            if nfol:
                if os.path.exists(nfol):
                    settings.write("New-Project-Folder", nfol)
                else:
                    print("\033[1;31m"+talk.text("failed"))
                    
        ##############
            
        elif command == "new_project":
            if not settings.read("New-Project-Folder"):
                print("\033[1;33m"+talk.text("pm-do-new-project-error"))
            
            #if folder is configured
            else:
                nproj = input("\033[1;33m "+talk.text("Name")+" : ")
                
                if pm_project.new(nproj):
                    print("\033[1;32m"+talk.text("checked"))
                else:
                    print("\033[1;31m"+talk.text("failed"))
                
            
        ##############
            
        elif command == "projects_list":
            # Getting list of available projects
            for p in pm_project.get_list():    
                print("\033[1;35m "+p)
        
        ##############
        
        elif command == "project":
            
            n = input("\033[1;33m : ")
            print("\033[1;35m "+talk.text("Wait"))
            pm_project.load(n)
            
        
        ##############
        
        elif command == "scan":
            print("\033[1;35m "+talk.text("Wait"))
            for proj in pm_project.scan():
                print("\033[1;35m "+proj)
                
        
        ##############
            
        elif command == "convert":
            print("\nNot Implemented yet\n") 
        
        ## FAIL ##
        
        elif command != "":
            print("\033[1;31m"+talk.text("failed"))
            
            
    print("\033[1;m") #return terminal to normality
