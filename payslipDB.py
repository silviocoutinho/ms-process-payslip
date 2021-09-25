import json
import requests
import psycopg2
import re
import os
import threading

from dotenv import load_dotenv
from Payslip import Payslip


load_dotenv()

USERDB = os.getenv("USERDB")
DB = os.getenv("DB")
PASSDB = os.getenv("PASSDB")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT ")

#Create Thread that will use to store data in database
class storePayslipThread (threading.Thread):
        def __init__(self, threadID, payslip):           
            try:
                self.conn = psycopg2.connect(user = USERDB,
                                  password = PASSDB,
                                  host = DB_SERVER,
                                  port = DB_PORT,
                                  database = DB)
                self.cur = self.conn.cursor()                
                self.threadID = threadID
                self.payslip = payslip            
                
                threading.Thread.__init__(self)
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
                exit()
                       
        def run(self):
            print("self.paysplip: ===>>>>>", self.payslip)
            insertNewPayslip(self.conn, self.cur, self.payslip)

#=========Grava um novo registro=========
def insertNewPayslip(conn, cur, payslip):
  
    sqlString = """INSERT INTO holerites(employee_registration, month, year, type, "fileNamePayslip") VALUES (%s,%s,%s,%s,%s)"""
    dataToStore = (payslip.employee_registration, payslip.month, payslip.year, payslip.typePayslip, payslip.fileNamePayslip)

    try:
        cur.execute(sqlString, dataToStore)
        conn.commit()
    except(Exception, psycopg2.Error) as error :
        print ("Error while store payslip data:  ===>", error)
    

#=======Fim grava um novo registro

#paysplip=Payslip(299, "10", "2011", 1, "teste10.pdf")

#insertNewPayslip(paysplip)