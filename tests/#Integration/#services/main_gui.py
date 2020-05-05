
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.gui.gui_server import run_gui_server

if "__main__" == __name__:
    run_gui_server()
