FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3.11
RUN apt install -y python3.11-venv
RUN mkdir /home/app
RUN apt-install python3.11-venv

VOLUME ["/home/app"]

WORKDIR /home/app

RUN source env/bin/activate
RUN python3.11 -m pip install --upgrade pip setuptools virtualenv

RUN export USE_X11=1
RUN apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
RUN apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good
RUN apt-get install -y software-properties-common
RUN apt install -y curl
RUN apt-get update
# RUN add-apt-repository ppa:kivy-team/kivy \n
RUN apt-get update
RUN curl https://nodejs.org/dist/v18.16.0/node-v18.16.0-linux-x64.tar.xz -O
RUN apt install -y xz-utils
RUN tar -xf node-v18.16.0-linux-x64.tar.xz
RUN cp -r node-v18.16.0-linux-x64/{bin,include,lib,share} /usr/
RUN export PATH=/usr/node-v18.16.0-linux-x64/bin:$PATH
# RUN apt install -y nodejs
RUN apt install -y npm
RUN npm install -g @ionic/cli
# RUN apt-get install -y python3-kivy
# RUN apt-get install kivy-examples
# RUN python3.11 -m pip install Django
# RUN python3.11 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN python3.11 -m pip install -r ../code/requirements.txt

RUN python3.11 manage.py makemigrations
RUN python3.11 manage.py migrate
RUN python3.11 manage.py runserver 0.0.0.0:8000