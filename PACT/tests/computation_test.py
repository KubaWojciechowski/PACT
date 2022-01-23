import pandas as pd
import os

from PACT.src.computation import runModeller, compute_cross_model_interactions_concurently, cross_model


def test_runModeller():
    pathToAlignmentFile = '/PACT/PACT/tests/alignment.pir'
    pathToOutputDirectory = 'results'
    result = runModeller(pathToAlignmentFile, pathToOutputDirectory)
    assert(os.path.exists(pathToOutputDirectory))

def test_cross_model():
    inputFilePath = '/PACT/PACT/tests/example.csv'
    outputFolderPath = 'crossModelResults'
    data = pd.read_csv(inputFilePath)

    seq_list1 = data['seq1']
    seq_list2 = data['seq2']

    for i in range(len(seq_list1)):
        seq1 = str(seq_list1[i])
        seq2 = str(seq_list2[i])
        outputFolderPath = 'crossModelResults'+str(i)
        cross_model(seq1,seq2, outputFolderPath)
        assert(os.path.exists(outputFolderPath))

def test_compute_cross_model_interactions_concurently():
    inputFilePath = '/PACT/PACT/tests/example.csv'
    outputFolderPath = 'crossModelResults'
    inputData = pd.read_csv(inputFilePath)
    compute_cross_model_interactions_concurently(inputData, outputFolderPath)
    assert(os.path.exists(outputFolderPath))