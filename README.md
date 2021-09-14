![Alt text](logo_v1_bg.png)
## Requirements
PACT is a computational pipeline for prediction of amyloid cross-interactions. It uses poular molecular modeling software, in oreder to use it you need to install:
* Modeller (tested with 9.24 but should work with other versions too)
* Python3
As well as some Python packages:
* Numpy
* Pandas
* Biopython
## Input
PATH takes as an input csv file with the folowing columns: 

interactor,seq1,interactee,seq2

Where interactor and interactee are the names, and seq1 and seq2 are sequences of interacting proteins in fasta format
## Running PACT
You can run PACT as any other Python script by typeing:
`python pact_1.0.py -i <input_file> -o <output_directory>`

To run with docker use:
``` shell
./buildDocker.sh # to build docker container
./runDocker.sh # to run docker container
```
## PACT output
As PACT perform structural modeling which is computationaly expensive it might take a while to get your results. PACT output contains files containing energies and classification as well as directories for each protein fragment from input. Each of them have directories for molecular models for each of possible structural classes.
