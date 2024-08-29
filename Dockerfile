FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive" 
ENV TZ="Asia/Kolkata"

RUN apt-get update
RUN apt-get install -y python3 build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
RUN apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential


RUN apt-get install -y wget

# RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb

# RUN apt-get install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb

EXPOSE 8000

ADD wild_sugar /wild_sugar
WORKDIR /wild_sugar

RUN pip3 install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8


CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]

