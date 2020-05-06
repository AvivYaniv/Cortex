import sys
import subprocess

WAIT_TO_END_DEFAULT = True

def run_bash_scipt(script_path, wait_to_end=None, show_output=None):
    wait_to_end = wait_to_end if wait_to_end else WAIT_TO_END_DEFAULT
    
    show_output = show_output if (show_output and wait_to_end) else True
    
    process = subprocess.Popen(         \
                script_path,            \
                shell=True,             \
                stdout=subprocess.PIPE, \
                stderr=subprocess.STDOUT)
    
    if show_output:
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8'))        
    
    if wait_to_end:
        process.wait()
        return process.returncode
