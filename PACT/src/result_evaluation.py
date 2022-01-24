import pandas as pd
import numpy as np
import os
import subprocess


def create_meta_file(seq_list1, seq_list2, outputFolder : str):
    if(len(seq_list1) != len(seq_list2)):
        return
    # Probably parametrized by output path
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    meta_file_path = outputFolder + '/' + 'meta.csv'
    meta_file = open(meta_file_path, 'w')
    print("seq,length", file=meta_file)
    for i in range(len(seq_list1)):
        name = "pair_" + str(i)
        length = (len(seq_list1[i])+len(seq_list2[i]))/2
        print("%s,%f" % (name, length), file=meta_file)
    meta_file.close()
    return meta_file_path

def run_script(script):
    
    p = subprocess.Popen(script, stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

def compute_energies(inputDirectory : str):
    '''This should probably do what currently does data.sh script.'''
    # how we now that ../scripts/data.sh is there? ; If I were to pip install pact then I should be able to use it anywhere
    cwd = os.getcwd()
    os.chdir(inputDirectory)
    os.link('/PACT/scripts/data.sh', inputDirectory+'/'+'data.sh')

    run_script("bash data.sh > energy.csv")
    os.chdir(cwd)

    return inputDirectory + '/' + 'energy.csv'

def find_minimum_energies(energies : pd.DataFrame, meta_file : pd.DataFrame, threshold):
    '''Numpy manipulations from compute_scores should be here.'''
    data = pd.merge(energies, meta_file, on='seq')

    min_e = data.loc[data.groupby('seq')['dope'].idxmin()]
    min_e['ndope'] = min_e['dope']/min_e['length']
    min_e['prediction'] = np.where(min_e['ndope'] < threshold, 1, 0)

    return min_e.values

def save_energies_to_file(results : np.ndarray, initial_data : pd.DataFrame, output_folder : str):
    names_list1 = initial_data['interactor']
    names_list2 = initial_data['interactee']
    result_file_path = output_folder + '/' + 'results.csv'
    results_file = open(result_file_path, 'w')

    # should be behind verbose flag
    # because we don't need it in web application
    print('pair,interactor,interactee,score,classification', file=results_file)
    for i in range(len(results)):
        #print("%d,%s,%s,%s,%s,%3.2f,%d" % (i, names_list1[i], seq_list1[i], names_list2[i], seq_list2[i],  results[i,-2],results[i,-1]))
        print("%d,%s,%s,%3.2f,%d" % (
            i, names_list1[i], names_list2[i],  results[i, -2], results[i, -1]), file=results_file)

    results_file.close()
    return result_file_path


def compute_scores(data: pd.DataFrame, output_path: str,threshold):
    # Scoring
    energyFilePath = compute_energies(output_path)
    energies = pd.read_csv(energyFilePath)
    meta_file = pd.read_csv(output_path + '/' + "meta.csv")
    min_energies = find_minimum_energies(energies, meta_file, threshold)
    return save_energies_to_file(min_energies, data, output_path)