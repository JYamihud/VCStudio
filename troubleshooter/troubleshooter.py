# THIS FILE IS A PART OF VCStudio
# PYTHON 3


import os
w, h = os.get_terminal_size() 

from settings import settings
from settings import talk
from troubleshooter import fix

def cls():
    #cleaning the terminal
    os.system("clear")
    
    global w
    global h
    
    w, h = os.get_terminal_size()
    if (w % 2) == 0:
        w = w - 1


def output(form, text=""):
    #Basically a fancy print() function
    while len(text) < w:
        text = text + " "
        
    print(form + text)

# COFIGURING LANGUAGE
def lang_setting():
    
    
    
    title = "TYPE YOUR LANGUAGE AND HIT ENTER"
    
    while True:
        
        cls()
        
        #getting the configuration
        language = settings.read("Language")
        
        # Testing if I cal load the language file.
        try:
            open("settings/languages/"+language+".data")
            return
        except:
            pass
        
        talk.alert("Select Language. Look in console.")
        
        # Getting list of available languages
        all_langs = os.listdir("settings/languages/")
        
        # Filtering all the unnesesary garbage
        r = []
        for lang in all_langs:
            if lang.endswith(".data"):
                r.append(lang.replace(".data", ""))
        all_langs = sorted(r)
        
        # Counting them
        len_langs = len(all_langs)
        
        
        
        
        output("\033[1;44m")
        
        #Title
        
        output("\033[1;44m", \
        " " * int(round((w-len(title))/2)) \
        + title + \
        " " * int((w-len(title))/2) \
        )
        
        output("\033[1;44m")
        
        for raws in range(int((h-5-len_langs)/2)):
            output("\033[1;40m")
        
        for lang in all_langs:
            
            output("\033[1;40m", \
            " " * int(round((w-len(lang))/2)) \
            + lang + \
            " " * int((w-len(lang))/2) \
            )
        
        
        for raws in range(int((h-5-len_langs)/2)):
            output("\033[1;40m")
        
        
    
        print("\033[1;m")
        
        # Trying to write language setting.
        command = input()
        if command != "":
            if command not in all_langs:
                title = "THERE IS NO " + command + " FILE"
            else:
                settings.write("Language",command)
                return

        
lang_setting()



def modules_test(Modules, title, setting):
    
    
    # TESTING THAT MODULES ARE INSTALLED CORRECTLY
    
    
        
    cls()
    
    import time  # IK it's crazy but user needs to understand what's
                 # going on. So there be some delay between them.
    
    
    
    
    title = talk.text(title)
        
    
    def drawmodules():
        
        cls()
        
        
        output("\033[1;44m")
    
        output("\033[1;44m", \
        " " * int((w-len(title))/2) \
        + title + \
        " " * int((w-len(title))/2) \
        )
        
        output("\033[1;44m")
        
        for raws in range(int((h-5-len(Modules))/2)):
            output("\033[1;40m")
        
        for mod2 in Modules:
        
            if Modules[mod2] == None:
                
                ans = mod2
                    
                output("\033[1;40m", " "+ans)
            
            elif Modules[mod2] == True:
                ans = mod2 + " "*int(w/2-len(mod2)) + talk.text("checked")
                    
                output("\033[1;42m", " "+ans)
            else:
                
                ans = mod2 + " "*int(w/2-len(mod2)) + talk.text("failed")
                    
                output("\033[1;41m", " "+ans)
                
                
        for raws in range(int((h-6-len(Modules))/2)):
            output("\033[1;40m")
    
    errors = 0
    for mod in Modules:
        
        drawmodules()
            
        try:
            try:
                
                exec( "import " + mod)
                Modules[mod] = True
                
            except:
                Modules[mod] = False
                errors = errors + 1
                
        except:
            pass
        time.sleep(0.1)        
        
            
    drawmodules()
    
    if errors:
        
        talk.alert(talk.text("missingmodulenotification"))
        
        title = str(errors)+" "+talk.text("missingmoduleserror")
    
        output("\033[1;40m\033[1;31m", \
        " " * int((w-len(title))/2) \
        + title + \
        " " * int((w-len(title))/2) \
        )
        
        #fix thing
        print("\033[1;m")
        command = input()
        
        if command == "Fix":
            fix.autofix(Modules)
    
    else:
        #if no errors
        settings.write(setting, "Checked-by-troubleshooter")
        
    print("\033[1;m")
        

if not settings.read("Python-is-good"):

    Modules = {
            "os":None,
            "gi":None,
            "gi.repository.Gtk":None,
            "cairo":None,
            "PIL":None,
            "PIL.Image":None, 
            "subprocess":None,
            "datetime":None,
            "sys":None,
            "urllib":None,
            "urllib3":None,
            "socket":None
            }

    modules_test(Modules, "checkingpythonmodules", "Python-is-good")

if not settings.read("VCStudio-is-good"):

    OwnModules = {
            "settings.settings":None,
            "settings.talk":None,
            "troubleshooter.troubleshooter":None,
            "troubleshooter.fix":None,
            "project_manager.pm_console":None, 
            }

    modules_test(OwnModules, "checkingpartsoftheprogramm", "VCStudio-is-good")



































