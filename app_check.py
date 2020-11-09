# used to run the main script
import os.path
from os import path

import mypath

file_status = mypath.data_folder / "status.txt"
file_main = mypath.data_folder / "main.py"


if path.exists(file_status):  # check if status.txt exists
    f = open(file_status, 'r')
    pid = f.readline()
    pid = int(pid)
    # print(pid)
    f.close()

    try:  # check if PID on status.txt exists
        os.kill(pid, 0)
    except OSError:  # if not then create. #wasn't working on a separete function
        f = open(file_status, "w+")  # write the PID to status.txt
        f.write(str(pid))
        f.close()
        # run main script if status.txt doesn't exist
        exec(open(file_main).read())
    else:  # if running
        print('discord bot script is running')
        exit('exiting...')
else:  # wasn't working on a separete function
    pid = os.getpid()
    f = open(file_status, "w+")  # write the PID to status.txt
    f.write(str(pid))
    f.close()
    # run main script if status.txt doesn't exist
    exec(open(file_main).read())
