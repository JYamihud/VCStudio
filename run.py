# THIS FILE IS A PART OF VCStudio
# PYTHON 3
import sys

# If any arguments
console_force = False
if len(sys.argv) > 1 and sys.argv[1] == "-c":
    console_force = True

# Importing various things
from settings import settings
from settings import talk



try:    
    
    # The :) I'm Happy To See You
    talk.alert(talk.text("imissedyouwelcommessage"))    
    
    if not console_force:
        # I'm importing it here so it wont give problems on non GTK systems.
        from project_manager import pm_gtk
        pm_gtk.run()
    
    else:
        from project_manager import pm_console
        pm_console.run()
    

except Exception:
    raise()
    # If some mistake happened

    # Testing the software
    from troubleshooter import troubleshooter
    
    if not settings.read("Python-is-good"):
        # Project Manager console version
        from project_manager import pm_console
        pm_console.run()
