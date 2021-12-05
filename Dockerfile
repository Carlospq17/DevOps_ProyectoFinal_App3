FROM python:3.8

#copiamos el actual directorio en el directio root del contenedor
WORKDIR /app
COPY . /app
#instalamos todas las dependencias necesarias para poder ejecutar el programa
RUN pip install mysql-connector-python
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN apt-get update
RUN apt-get install -y iputils-ping

#Corremos el programa
CMD python3 main.py && tail -f /dev/null