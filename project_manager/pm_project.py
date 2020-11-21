# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# this file handles language
import os
import subprocess
from settings import settings
from settings import talk


def new(name):
    
    # Removing all the bad characters
    
    name.replace("/","_").replace(" ", "_")\
    .replace('"',"_").replace("(","_").replace(")","_").replace("'","_")\
    .replace("[","_").replace("]","_").replace("{","_").replace("}","_")
    
    
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


def scan():
    
    ret = []
    
    #scan the system for "ast/chr" a folder that accurs in a project
    for i in [x[0] for x in os.walk("/")]:
        if i.endswith("/ast/chr"):
            ret.append(i.replace("/ast/chr", ""))
            register_project(i.replace("/ast/chr", ""))
    
    return ret
    
def load(path):
    
    #first let's figure out if it's an old Blender-Organizer
    #or a new VCStudio project.
    
    #if new
    if not is_legacy(path):
        print(" Not Yet Implemented VCStudio ")
    
    #old organizer
    else:
        if not os.path.exists(path+"/MAIN_FILE"):
            n = "blender-organizer"
        else:
            n = open(path+"/MAIN_FILE")
            n = n.read()
        
        #let's look if there is python2 since it's legacy software
        if not os.system("python2 -V") == 0:
            return "No python2"
        
        #loading the python2 thingy
        sh = open("/tmp/run_legacy_organizer.sh", "w")
        sh.write("cd "+path+"\n")
        sh.write("python2 "+n+"\n")
        sh.write('read -p ""')
        sh.close()
        
        if not os.path.exists(path+"/MAIN_FILE"):
            os.system("gnome-terminal -- sh /tmp/run_legacy_organizer.sh")
        else:
            subprocess.Popen(["sh", "/tmp/run_legacy_organizer.sh"])
    
        
        
def is_legacy(project):
    
    # This function checks whether a given project is a Legacy ( Blender -
    # Organizer ) project.
    
    if not os.path.exists(project+"/set"):      
        return True
    else:
        return False
    
    
