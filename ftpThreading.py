from ftplib import FTP

from dotenv import load_dotenv
import os
import threading

load_dotenv()


FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
FTP_PORT = os.getenv("FTP_PORT")

class myThread (threading.Thread):
        def __init__(self, threadID, src, counter, image_name):
            ###############
            #Add ftp connection here!
            self.ftp = FTP(FTP_HOST, FTP_USER, FTP_PASS)   # connect to host, default port
            self.ftp.login()               # user anonymous, passwd anonymous@   
            ################
            self.threadID = threadID
            self.src = src
            self.counter = counter
            self.image_name = image_name
            threading.Thread.__init__(self)
        def run(self):
            uploadFile(self.src, self.image_name)

def uploadFile(src, image_name):
    f = open(src, "rb")            
    self.ftp.storbinary('STOR ' + image_name, f)
    f.close()

dirname = "09"
i = 1   
threads = []

for image in os.listdir(dirname):
    print(image)
    if os.path.isfile(dirname + image):
        thread = myThread(i , dirname + image, i, image )   
        thread.start()
        threads.append( thread )        
        i += 1  

for t in threads:
    t.join()