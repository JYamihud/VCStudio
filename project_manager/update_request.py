# THIS FILE IS A PART OF VCStudio
# PYTHON 3

import urllib3

# This file requests a update from the GITHUB reposytory containing the update
# information.

filepath = "https://raw.githubusercontent.com/JYamihud/VCStudio/main/settings/update.data"

# Those 3 lines basically retrieve the file from the internet and output them 
# to the console. Which I'm catching in the update_reader.py using a Pipe.

try:
    http = urllib3.PoolManager()
    resp = http.request('GET', filepath)
    print(resp.data.decode('utf-8'))
except:
    data = open("settings/update.data")
    print(data.read())

print("END")
