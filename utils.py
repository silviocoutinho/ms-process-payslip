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

def removeFile(fileName):
    try:
        if os.path.exists(fileName):
            os.remove(fileName)
        else:
            print('Error when try to remove file:', fileName)
    except OSError as e:
        print("Error: %s : %s" % (fileName, e.strerror))
