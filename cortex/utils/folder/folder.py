
import os, shutil

def count_folders_subfolders(folder):
    return len([root for root in os.listdir(folder)])

def delete_under_folder(folder):    
    shutil.rmtree(folder, ignore_errors=True)
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
