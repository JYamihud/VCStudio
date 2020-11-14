# THIS FILE IS A PART OF VCStudio
# PYTHON 3

import sys

# Testing the software
from troubleshooter import troubleshooter

# Importing various things
from settings import settings
from settings import talk
from project_manager import pm_console
from project_manager import pm_gtk

# The :) I'm Happy To See You
talk.alert(talk.text("imissedyouwelcommessage"))

# If any arguments
console_force = False
if len(sys.argv) > 1 and sys.argv[1] == "-c":
    console_force = True


# Project Manager console version
if not settings.read("Python-is-good") or console_force:
    pm_console.run()
else:
    pm_gtk.run()
