![Alt text](logo_v1_bg.png)
## Requirements
PACT is a computational pipeline for prediction of amyloid cross-interactions. It uses poular molecular modeling software, in oreder to use it you need to install:
* Modeller (tested with 9.24 but should work with other versions too, You need to provide licence key, put it into docker/dockerfile: "ENV KEY_MODELLER" XXXXX") 
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
You can run PACT in docker. First build the container:
``` shell
cd docker
./buildDocker.sh
```
Then from project root folder run:
``` shell
./docker/runDocker.sh
```
And then run following command to build PACT as package inside the container:
``` shell
bash rebuild.sh
```
You can now run PACT by calling it's module:

`python -m pact_cli.cli --input_file examples/example.csv --output_dir examples/output`

## PACT output
As PACT perform structural modeling which is computationaly expensive it might take a while to get your results. PACT output contains files containing energies and classification as well as directories for each protein fragment from input. Each of them have directories for molecular models for each of possible structural classes.
