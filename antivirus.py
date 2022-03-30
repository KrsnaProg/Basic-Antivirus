from operator import ge
import psutil
import os
import subprocess

# Iterate over all running process
def get_running_process_dict():
    process_dict = {}
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            if not processName in process_dict:
                process_dict[processName.lower()] = [processID]
            else:
                process_dict[processName].append(processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass    
    return process_dict

#get cuurent working directory and store it in dir_path
dir_path = os.path.dirname(os.path.realpath(__file__))

#get process list
proc_dict = get_running_process_dict()

# Open black.list and get the proccess names which we don't want, then terminating it if it is running.
with open(dir_path+'\\black.list', 'r') as f:
    is_terminated = False
    black_list = f.read().split('\n')
    for black_proc in black_list:
        if black_proc+'.exe' in proc_dict.keys():
            proc_ans = subprocess.Popen('taskkill /F /IM '+black_proc+'.exe /T', shell=True, stdout=subprocess.PIPE)
            is_terminated = True
            print('I terminated', black_proc)
    if not is_terminated:
        print('Everything is good!')