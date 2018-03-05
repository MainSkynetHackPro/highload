From ubuntu:16.04

WORKDIR /app

RUN apt-get update &&\
        apt-get install -y nginx &&\
        apt-get install -y python &&\
        apt-get install -y jython

ADD server.py server.py
ADD core core
ADD httpd.conf httpd.conf
ADD utils utils
ADD index.html /var/www/html
ADD docker.nginx.conf /etc/nginx/sites-enabled/nginx.conf