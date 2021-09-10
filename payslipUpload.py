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
        
        handler.encoding = "utf-8"      
    except Exception:        
        print('Não foi possivel conectar ao servidor FTP')
    return handler


def disconnectClient(handler):
    try:
        handler.quit()
    except Exception:
        print('Erro ao desconectar')
        return None
    print('operação efetuada com sucesso')


def upload(handler, name, path):
    try:        
        handler.cwd(path)
        with open(name, "rb") as file:        
            handler.storbinary(f"STOR {filename}", file)
    except Exception:        
        print('Erro ao subir o arquivo ao servidor')
        return None
    print('Arquivo salvo')

############################################################

ftp = connectClient(FTP_USER, FTP_PASS, FTP_HOST, FTP_PORT)

filename = "Folhatemp.pdf"
upload(ftp, filename, "holerites/2021")

disconnectClient(ftp)

