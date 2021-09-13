from splitPdf import pdfSplitter, convertPdfToCsv, interateSeries, removeHyphen

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
    mode = 0o777
    os.mkdir(month, mode)

    #Create Dictionary to Store information about payslips
    paysplipInformation = {}



    for index, value in enumerate(employeeRegistration):
        value = value + month + year + SECRET_TO_HASH        
        hashName = hashlib.md5(value.encode())
        pdfSplitter(file, hashName.hexdigest(), index, month) 


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

        urlFile = "http://" + jsonObject["urlServer"] + "/" + jsonObject["storeFilePath"]  + "/" + jsonObject["fileName"]
        month = jsonObject["month"] 
        year  = jsonObject["year"]
        getPayslipFromFTP(urlFile)
        processPayslip('Folhatemp.pdf', month, year)

       
        

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