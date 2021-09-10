import json
import requests
import psycopg2
import re

from Ponto import Ponto

import os

load_dotenv()

USERDB = os.getenv("USERDB")
DB = os.getenv("DB")
PASSDB = os.getenv("PASSDB")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT ")

conectado = False

try:
    conn = psycopg2.connect(user = USERDB,
                                  password = PASSDB,
                                  host = DB_SERVER,
                                  port = DB_PORT,
                                  database = DB)
    cur = conn.cursor()
    conectado = True

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    exit()

