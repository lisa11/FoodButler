# Helper python program to help initiate the syncal.py program
# This file is entirely original

from subprocess import call
import json

def sync(time_dict):
    '''
    helper function to call python2 syncal.py
    '''

    with open("time_dict.json", "w") as f:
        f.write(json.dumps(time_dict))

    call("python2 syncal.py", shell=True)
    call("rm time_dict.json", shell=True)