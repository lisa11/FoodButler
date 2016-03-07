# Helper python program to help initiate the syncal.py program

from subprocess import call
import json

def sync(start_date):
    '''
    helper function to call python2 syncal.py
    '''

    with open("start_date.json", "w") as f:
        f.write(json.dumps(start_date))

    call("python2 syncal.py", shell=True)