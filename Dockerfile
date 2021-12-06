FROM python:3.8

#copiamos el actual directorio en el directio root del contenedor
WORKDIR /root
COPY . /root

#creamos el folder donde se guardaran los archivos csv de las tablas
RUN mkdir punto_de_venta

#instalamos todas las dependencias necesarias para poder ejecutar el programa
RUN python3 -m pip install mysql-connector-python
RUN python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN apt-get update
RUN apt-get -y install cron

#para temas demostrativos y de testeo se instalan las siguientes herramientas
RUN apt-get install -y iputils-ping
RUN apt-get install nano

#configuramos el job que realiza el crontab
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN touch /var/log/cron.log

#corremos el programa utilizando el crontab
ENTRYPOINT cron && tail -f /var/log/cron.log