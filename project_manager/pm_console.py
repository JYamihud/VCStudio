# THIS FILE IS A PART OF VCStudio
# PYTHON 3

# This a console project manager.

import os
w, h = os.get_terminal_size() 

from settings import settings
from settings import talk

def cls():
    #cleaning the terminal
    os.system("clear")
    
def run():
    
    cls()
    print("\033[1;33m\n   VCStudio - Console \n")
    
    print("\033[1;32m"+talk.text("PMConsoleExplanation")+"\n")
    
    
    while True:
        command = input("\033[1;35m : \033[1;m")
        
        # exit
        
        if command == "exit":
            cls()
            exit()
    
        elif command == "help":
            
            print("\033[1;32m"+talk.text("pm_console_help")+"\n")
    
        elif command == "set_language":
            print("\nNot Implemented yet\n")
        
        elif command == "projects_list":
            print("\nNot Implemented yet\n")    
        
        elif command == "new_project":
            print("\nNot Implemented yet\n")   
        
        elif command == "project":
            print("\nNot Implemented yet\n") 
        
        elif command == "scan":
            print("\nNot Implemented yet\n") 
            
        elif command == "convert":
            print("\nNot Implemented yet\n") 
        
        
    print("\033[1;m") #return terminal to normality
