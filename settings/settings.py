# THIS FILE IS A PART OF VCStudio
# PYTHON 3

import os

def read(setting):
    #opening the file
    data = open("settings/settings.data")
    data = data.read()
    data = data.split("\n")
    #finding the keyword
    for line in data:
        if line.startswith(setting):
            return convert(line.replace(setting+" = ", ""))
    
    return False

def write(setting, value):
    
    # Making sure that the value is string'
    value = str(value)
    
    #opening the file
    data = open("settings/settings.data")
    data = data.read()
    data = data.split("\n")
    
    #making a new file
    ndata = open("settings/settings.data", "w")
    
    
    #finding the keyword
    found = False
    for line in data:
        if line.startswith(setting):
             line = setting+" = "+str(value)
             found = True
        if line != "":
            ndata.write(line+"\n")
    
    if not found:
        ndata.write(setting+" = "+str(value)+"\n")
        
    
    ndata.close()
    
    
def list_languages():
    
    # Getting list of available languages
    all_langs = os.listdir("settings/languages/")
    
    # Filtering all the unnesesary garbage
    r = []
    for lang in all_langs:
        if lang.endswith(".data"):
            r.append(lang.replace(".data", ""))
    all_langs = sorted(r)
    
    return all_langs

def load_all():
    
    # This function will preload everything for the settings file into the RAM
    # so if something has to be checked on every frame. I would not need to deal
    # with it constantly. But rather have a ddictionary in the RAM to which I
    # am going to refer at each frame / instance etc.
    
    ret = {}
    
    # Opening the file.
    data = open("settings/settings.data")
    data = data.read()
    data = data.split("\n")
    
    # Parsing the file.
    for d in data:
        if d:
            ret[d[:d.find(" = ")]] = convert(d[d.find(" = ")+3:])
    
    # Returning
    return ret

def convert(string):
    
    # This function will convert a string of value. Into the value it self.
    # For exmple if it has float or boolean (True, False, None) data in the
    # settings file. So it's gonna be easier to parse later on. 
    
    # Trying fload
    try:
        string = float(string)
    except:
        
        # Trying boolean
        if string == "True":
            string = True
        elif string == "False":
            string = False
        elif string == "None":
            string = None
    # That's it
    return string
        
