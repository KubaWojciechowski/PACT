import os
import pandas as pd
import numpy as np
from PACT.src.result_evaluation import compute_energies,compute_scores,create_meta_file,find_minimum_energies
from PACT.src.computation import compute_cross_model_interactions_concurently

def test_create_meta_file():
    inputFilePath = '/PACT/PACT/res/example.csv'
    outputFolderPath = 'metaFileFolder'
    data = pd.read_csv(inputFilePath)

    seq_list1 = data['seq1']
    seq_list2 = data['seq2']
    meta_file_path = create_meta_file(seq_list1, seq_list2,outputFolderPath)
    assert(os.path.exists(meta_file_path))

def test_compute_energies():
    inputFilePath = '/PACT/PACT/res/example.csv'
    outputFolderPath = '/PACT/energiesFileFolder'
    data = pd.read_csv(inputFilePath)

    compute_cross_model_interactions_concurently(data, outputFolderPath)
    energy_file_path = compute_energies(outputFolderPath)
    assert(os.path.exists(energy_file_path))

def test_find_minimum_energies():
    inputFilePath = '/PACT/PACT/res/example.csv'
    outputFolderPath = '/PACT/energiesFileFolder01'
    data = pd.read_csv(inputFilePath)

    seq_list1 = data['seq1']
    seq_list2 = data['seq2']

    meta_file_path = create_meta_file(seq_list1,seq_list2,outputFolderPath)
    compute_cross_model_interactions_concurently(data, outputFolderPath)
    min_energies = find_minimum_energies(data,meta_file_path,236)
    assert(min_energies.mean() > 0)


def test_compute_scores():
    inputFilePath = '/PACT/PACT/res/example.csv'
    outputFolderPath = '/PACT/energiesFileFolder01'
    data = pd.read_csv(inputFilePath)

    result_file_path = compute_scores(data,outputFolderPath,236)
    assert(os.path.exists(result_file_path))