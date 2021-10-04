from Payslip import Payslip
from splitPdf import pdfSplitter, convertPdfToCsv, interateSeries, removeHyphen
from payslipUpload import ftpThread
from payslipDB import storePayslipThread
from utils import createFolder, removeFolder

import pika, sys, os, json

import tabula
import pandas as pd
import numpy as np
import hashlib

import requests

from dotenv import load_dotenv

load_dotenv()

queueName = os.getenv("QUEUE_NAME")
RABBITMQ_SERVER = os.getenv("RABBITMQ_SERVER")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
URL_FILE_SERVER = os.getenv("URL_FILE_SERVER")
URL_PATH_FILES_STORED = os.getenv("URL_PATH_FILES_STORED")
SECRET_TO_HASH = os.getenv("SECRET_TO_HASH")



def processPayslip(file, month, year):
    # Main Function
    convertPdfToCsv(file, "csv")

    # Open CSV with pandas and create dataframe df
    df = pd.read_csv('Folha.csv', sep="\n", names=["A"])

    # Searching a specific part in csv and overwriting the dataFrame
    # This procedure will remove all data except personal data of employees
    df = df[df['A'].str.contains("Servidor\r")]

    # Remove String 'Servidor\r' from data
    df['A'] = df['A'].str.strip('Servidor\r')

    # Extract slice of String, getting just numbers of employee registration(matricula)
    df['B'] = df['A'].apply(lambda x: x[0:3])

    # Remove the hyphen
    df['result'] = df['B'].apply(lambda x: removeHyphen(x))
    df = df['result']

    # Create Array with result from dataFrame
    employeeRegistration = df.to_numpy()

    #Create Folder to Store files for the month
    createFolder(month)   
    
    #Create Dictionary to Store information about payslips
    objectJSONPayslip = {}

    for index, value in enumerate(employeeRegistration):        
        valueToEncode = value + month + year + SECRET_TO_HASH        
        hashName = hashlib.md5(valueToEncode.encode())
        objectJSONPayslip[value] = {"fileName": hashName.hexdigest()+".pdf", "month": month, "year":year, "employeeRegistration":value}
        pdfSplitter(file, hashName.hexdigest(), index, month)

    return objectJSONPayslip      
  


def getPayslipFromFTP(file):
    r = requests.get(file, allow_redirects=True)
    open('Folhatemp.pdf', 'wb').write(r.content)
    


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER, RABBITMQ_PORT))
    channel = connection.channel()

    channel.queue_declare(queue=queueName)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)        
        jsonObject = json.loads(body)
        print(jsonObject["fileName"])

        # "http://" +
        urlFile =  jsonObject["urlServer"] + "/" + jsonObject["storeFilePath"]  + "/" + jsonObject["fileName"]
        month = jsonObject["month"] 
        year  = jsonObject["year"] 
        description = jsonObject["description"]       
        getPayslipFromFTP(urlFile)
        objectJSONPayslip = processPayslip('Folhatemp.pdf', month, year)
       
        i = 1   
        threads = []
        
        print("Current working directory: {0}".format(os.getcwd()))
        pathSource = month
        pathDestination = "holerites" + "/" + year
        for payslip in objectJSONPayslip:  
            fileName                = objectJSONPayslip[payslip]["fileName"]
            employeeRegistration    = objectJSONPayslip[payslip]["employeeRegistration"]      
            sourceFile      =  pathSource       + "/" + fileName
            destinationFile =  pathDestination  + "/" + fileName
            newPayslip = Payslip(employeeRegistration, month, year, description, 1, fileName)
            if os.path.isfile(sourceFile):
                thread = ftpThread(i , sourceFile, i,  destinationFile )   
                thread.start()
                threads.append( thread )        
                i += 1
                thread2 = storePayslipThread(i , newPayslip )   
                thread2.start()
                threads.append( thread2 )        
                i += 1    
        
        for t in threads:
            t.join()
        
        print(' [*] Files sended to Server!!!')
        #Remove Temp Folder
        removeFolder(pathSource)
        print(' [*] Waiting for messages. To exit press CTRL+C')

       
        

    channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)