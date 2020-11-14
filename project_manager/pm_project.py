# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# this file handles language
import os
from settings import settings
from settings import talk


def new(name):
    
    # This function makes a new project.
    
    # If there is not such a folder. As in the settings.
    if not os.path.exists(settings.read("New-Project-Folder")):
        return False
    
    # If there is a project folder, or a file with it's name.
    elif os.path.exists(settings.read("New-Project-Folder")+"/"+name):
        return False
        
    #If all good
    else:
        try:
            
            fn = settings.read("New-Project-Folder")+"/"+name
            
            os.mkdir(fn)
            os.mkdir(fn+"/rnd")
            os.mkdir(fn+"/dev")
            os.mkdir(fn+"/ast")
            os.mkdir(fn+"/pln")
            os.mkdir(fn+"/mus")
            os.mkdir(fn+"/set")
            
            for f in ["chr","loc","veh","obj"]:
                os.mkdir(fn+"/ast/"+f)
                os.mkdir(fn+"/dev/"+f)
            
            register_project(fn)
            
            return True
        
        # If it fails to create a project for some reason.    
        except:
            return False
            
            
def register_project(path):
    
    prevdata = ""
    
    try:
        data = open("project_manager/projects_list.data")
        prevdata = data.read()
    except:
        pass
    data = open("project_manager/projects_list.data", "w")
    if path not in prevdata:
        data.write(prevdata+path+"\n")
    else:
        data.write(prevdata)
    data.close()
    
    
def get_list():
    
    ret = []
    
    try:
        data = open("project_manager/projects_list.data")
        data = data.read()
        data = data.split("\n")
        
        for line in data:
            if os.path.exists(line):
                ret.append(line)
    except:
        pass
        
    return ret
