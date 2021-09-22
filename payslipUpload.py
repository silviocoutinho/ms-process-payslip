from ftplib import FTP

from dotenv import load_dotenv
import os
import threading

load_dotenv()


FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
FTP_PORT = os.getenv("FTP_PORT")

#Create Thread that will use to store files in ftp server
class ftpThread (threading.Thread):
        def __init__(self, threadID, src, counter, dst):
           
            try:
                self.ftp = FTP(FTP_HOST, FTP_USER, FTP_PASS)   # connect to host, default port
                self.threadID = threadID
                self.src = src
                self.counter = counter
                self.dst = dst
                threading.Thread.__init__(self)
            except Exception:
                print('Não foi possivel conectar ao servidor FTP')
                       
        def run(self):
            print("self.src: ===>>>>>", self.src)
            uploadFile(self.ftp, self.src, self.dst)


def uploadFile(ftp, src, dst):
    f = open(src, "rb")            
    ftp.storbinary('STOR ' + dst, f)
    f.close()





