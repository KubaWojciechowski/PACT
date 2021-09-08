FROM python:3.9-slim-bullseye
WORKDIR /PACT
ENV PYTHONHOME="/usr/local"
# Debian
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y wget libglib2.0-0
# python packages
RUN pip install numpy pandas biopython
# modeller
RUN wget https://salilab.org/modeller/10.1/modeller_10.1-1_amd64.deb
RUN env KEY_MODELLER=MODELIRANJE dpkg -i modeller_10.1-1_amd64.deb
RUN ln -s /usr/bin/mod10.1 /usr/bin/mod