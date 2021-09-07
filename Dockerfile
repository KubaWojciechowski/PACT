FROM python:3
WORKDIR PACT
# python packages
RUN yes | pip install numpy pandas biopython
# modeller
RUN wget https://salilab.org/modeller/10.1/modeller_10.1-1_amd64.deb
RUN env KEY_MODELLER=XXXX dpkg -i modeller_10.1-1_i386.deb
