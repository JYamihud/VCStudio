# THIS FILE IS A PART OF VCStudio
# PYTHON 3


import os
w, h = os.get_terminal_size() 

from settings import settings
from settings import talk

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
    
    


def autofix(Modules):
    print("Autofix not yet implemented")
    print("We need testing to implement it")
    print("Please contact us. https://github.com/JYamihud/VCStudio/issues")
    input()
