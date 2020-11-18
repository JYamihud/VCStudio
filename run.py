# THIS FILE IS A PART OF VCStudio
# PYTHON 3
import sys

# If any arguments
console_force = False
if len(sys.argv) > 1 and sys.argv[1] == "-c":
    console_force = True

try:
    
    # I'm importing it here so it wont give problems on non GTK systems.
    from project_manager import pm_gtk
    pm_gtk.run()

except:
    

    # Testing the software
    from troubleshooter import troubleshooter

    # Importing various things
    from settings import settings
    from settings import talk

    # The :) I'm Happy To See You
    talk.alert(talk.text("imissedyouwelcommessage"))

   
    # Project Manager console version
    if not settings.read("Python-is-good") or console_force:
        from project_manager import pm_console
        pm_console.run()
        exit()

