FROM python:3
RUN pip install --upgrade pip


RUN pip install PyPDF2  
RUN pip install tabula-py && pip install pandas 
RUN pip install numpy && pip install pika 
RUN pip install requests && pip install psycopg2
RUN pip install python-dotenv
RUN pip install --upgrade pandas


# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;
    
# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

RUN adduser  myuser
RUN mkdir -p /home/myuser/app
RUN chown myuser /home/myuser/app
RUN chmod 755  /home/myuser/app
USER myuser
WORKDIR /home/myuser/app
COPY . /home/myuser/app

CMD python payslipProcess.py