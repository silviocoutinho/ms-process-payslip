import tabula
import pandas as pd
import numpy as np
import os

from PyPDF2 import PdfFileWriter, PdfFileReader



def pdfSplitter(file, name, page, folder):
    
    inputPDF = PdfFileReader(file)
    outputPDF = PdfFileWriter()
    outputPDF.addPage(inputPDF.getPage(page))
    name = os.path.join(folder, name)
    with open(name + ".pdf", "wb") as output_stream:
        outputPDF.write(output_stream)

    

def convertPdfToCsv(file, format):
    dfs = tabula.convert_into(file, "Folha.csv", output_format=format, pages="all")
   

def interateSeries(series):
    for rownum,(indx,val) in enumerate(series.iteritems()):
        return searchCharMinus(val)

def removeHyphen(string):
    response=''
    for element in range(0, len(string)):
        if (string[element]) != '-':
            response = response + string[element]
    return response

