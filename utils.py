import os, shutil

#Create Folder to Store files for the month
def createFolder(path):
    mode = 0o777
    os.mkdir(path, mode)

def removeFolder(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))