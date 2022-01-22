import pandas as pd
import numpy as np
import os


def create_meta_file(seq_list1, seq_list2):
    if(len(seq_list1) != len(seq_list2)):
        return
    # Probably parametrized by output path
    meta_file = open('/meta.csv', 'w')
    print("seq,length", file=meta_file)
    for i in range(len(seq_list1)):
        name = "pair_" + str(i)
        length = (len(seq_list1[i])+len(seq_list2[i]))/2
        print("%s,%f" % (name, length), file=meta_file)
    meta_file.close()

def compute_energies():
    '''This should probably do what currently does data.sh script.'''
    # how we now that ../scripts/data.sh is there? ; If I were to pip install pact then I should be able to use it anywhere
    os.link('../scripts/data.sh', 'data.sh')

    # Can we do it without using bash scripts???
    run_script("bash data.sh > energy.csv")
    pass

def find_minimum_energies(energies : pd.DataFrame, meta_file : pd.DataFrame, threshold):
    '''Numpy manipulations from compute_scores should be here.'''
    data = pd.merge(energies, meta_file, on='seq')

    min_e = data.loc[data.groupby('seq')['dope'].idxmin()]
    min_e['ndope'] = min_e['dope']/min_e['length']
    min_e['prediction'] = np.where(min_e['ndope'] < threshold, 1, 0)

    return min_e.values

def save_energies_to_file(results : np.ndarray, initial_data : pd.DataFrame):
    names_list1 = initial_data['interactor']
    names_list2 = initial_data['interactee']
    results_file = open('results.csv', 'w')

    # should be behind verbose flag
    # because we don't need it in web application
    print('pair,interactor,interactee,score,classification', file=results_file)
    for i in range(len(results)):
        #print("%d,%s,%s,%s,%s,%3.2f,%d" % (i, names_list1[i], seq_list1[i], names_list2[i], seq_list2[i],  results[i,-2],results[i,-1]))
        print("%d,%s,%s,%3.2f,%d" % (
            i, names_list1[i], names_list2[i],  results[i, -2], results[i, -1]), file=results_file)

    results_file.close()


def compute_scores(data: pd.DataFrame, output_path: str,threshold):
    # Scoring
    os.chdir(output_path)

    compute_energies()
    energies = pd.read_csv("energy.csv")
    meta_file = pd.read_csv("meta.csv")
    min_energies = find_minimum_energies(energies, meta_file, threshold)
    save_energies_to_file(min_energies, data)