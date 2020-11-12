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
            return line.replace(setting+" = ", "")
    
    return False

def write(setting, value):
    
    
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
