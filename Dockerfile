FROM python:3.8

# Copiamos el actual directorio en el directio root del contenedor
WORKDIR /root
COPY . /root

# Creamos el folder donde se guardaran los archivos csv de las tablas
RUN mkdir punto_de_venta

# Instalamos todas las dependencias necesarias para poder ejecutar el programa
RUN python3 -m pip install mysql-connector-python
RUN python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN apt-get update
RUN apt-get -y install cron

# Para temas demostrativos y de testeo se instalan las siguientes herramientas
RUN apt-get install -y iputils-ping
RUN apt-get install nano

# Instalamos Filebeat
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && apt-get install filebeat
RUN cp -f /root/filebeat.yml /etc/filebeat/filebeat.yml

#Creamos el archivo para los logs del cron job
RUN touch /var/log/cron.log

# Configuramos el job que realiza el crontab
RUN (crontab -l ; echo "*/10 * * * * /usr/local/bin/python3 /root/main.py >> /var/log/cron.log 2>&1") | crontab

RUN chmod +x entrypoint.sh
CMD ["bash","entrypoint.sh"]