from ftplib import FTP

from dotenv import load_dotenv
import os

load_dotenv()


FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
FTP_PORT = os.getenv("FTP_PORT")


def connectClient(user, password, host, port):
    try:
        handler = FTP(host, user, password)       
             
    except Exception:        
        print('Não foi possivel conectar ao servidor FTP')
    return handler


def disconnectClient(handler):
    try:
        handler.quit()
    except Exception:
        print('Erro ao desconectar')
        return None
    print('FTP desconectado com sucesso')


def upload(handler, name, pathDestination, pathSource):
    try:     
         
        handler.cwd(pathDestination)
        fileName = os.path.join(pathSource, name)
        print("NAME: ",name)
        with open(fileName, "rb") as file:                  
            handler.storbinary(f"STOR {name}", file)  
       

    except Exception:        
        print('Erro ao subir o arquivo ao servidor')
        return None
    print('Arquivo salvo')

############################################################

#ftp = connectClient(FTP_USER, FTP_PASS, FTP_HOST, FTP_PORT)

#09/b89e1a4c4baaaa6f05b5e11424149871.pdf
#09/a4222dee349e33be6d0612857bcb0cf7.pdf
#09/1afe153c667dde7c108e5f0de64f2562.pdf
#1afe153c667dde7c108e5f0de64f2562
#filename = "1afe153c667dde7c108e5f0de64f2562.pdf"

#upload(ftp, filename, "holerites/2021", "09")

#disconnectClient(ftp)

