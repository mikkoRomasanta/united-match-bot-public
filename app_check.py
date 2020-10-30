# used to run the main script
import os.path
from os import path

if path.exists(
        "/home/ubuntux/Desktop/python-proj/status.txt"):  # check if status.txt exists
    print('discord bot script is running')
    exit('exiting...')
else:
    # run main script if status.txt doesn't exist
    exec(open("/home/ubuntux/Desktop/python-proj/main.py").read())
