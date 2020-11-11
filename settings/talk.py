# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# this file handles language
import os
from settings import settings

def text(var):
    
    
    data = open("settings/languages/"+settings.read("Language")+".data")
    data = data.read()
    data = data.split("]")
    
    #finding the keyword
    for line in data:
        if line.startswith("\n"+var):
            return line.replace("\n"+var+" = [", "")
    
    return "!Missing! "+var

def allert(message):
    
    os.system("notify-send -i "+os.getcwd()+'/tinyicon.png "VCStudio" "'+message+'"')
