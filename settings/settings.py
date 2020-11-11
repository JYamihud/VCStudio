# THIS FILE IS A PART OF VCStudio
# PYTHON 3


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
    print(setting, value)
    
    
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
