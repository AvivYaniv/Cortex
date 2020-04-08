import subprocess

WAIT_TO_END_DEFAULT = True

def run_bash_scipt(script_path, wait_to_end=None):
    wait_to_end = wait_to_end if wait_to_end else WAIT_TO_END_DEFAULT 
    process = subprocess.Popen(script_path, shell=True)
    if wait_to_end:
        process.wait()
        return process.returncode
