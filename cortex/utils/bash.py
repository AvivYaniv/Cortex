import subprocess

def run_bash_scipt(script_path, wait_to_end=True):
    process = subprocess.Popen(script_path, shell=True)
    if wait_to_end:
        process.wait()
        return process.returncode
