import subprocess

WAIT_TO_END_DEFAULT = True

def run_bash_scipt(script_path, wait_to_end=None, shell=None):
    wait_to_end = wait_to_end if wait_to_end else WAIT_TO_END_DEFAULT
    shell = shell if shell else True 
    process = subprocess.Popen(script_path, shell=shell)
    if wait_to_end:
        process.wait()
        return process.returncode
