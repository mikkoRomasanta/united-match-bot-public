import os
import signal

import mypath

file_status = mypath.data_folder / "status.txt"

f = open(file_status, 'r')
pid = f.readline()
pid = int(pid)
print(pid)
f.close()
os.kill(pid, signal.SIGKILL)
