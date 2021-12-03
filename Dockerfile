FROM python:3
RUN pip install --upgrade pip

RUN adduser  myuser
USER myuser
WORKDIR /home/myuser/app
COPY . /home/myuser/app

RUN pip install PyPDF2  
RUN pip install tabula && pip install pandas 
RUN pip install numpy && pip install pika 
RUN pip install requests && pip install psycopg2
RUN pip install python-dotenv

CMD python payslipProcess.py