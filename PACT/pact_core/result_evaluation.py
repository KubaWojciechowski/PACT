import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging

def create_meta_file(names1 : list, names2 : list, seq_list1 : list, seq_list2 : list, output_dir : Path) -> Path:
    if(len(seq_list1) != len(seq_list2)):
        return
    if not output_dir.exists():
        logging.info(f"Output directory {output_dir} does not exists, creating")
        os.mkdir(output_dir)
    meta_file_path = output_dir.joinpath('meta.csv')
    with open(meta_file_path, 'w') as meta_file_handle:
        print("name1,name2,seq,length", file=meta_file_handle)
        for i in range(len(seq_list1)):
            name = "pair_" + str(i)
            length = (len(seq_list1[i])+len(seq_list2[i]))/2
            print("%s,%s,%s,%f" % (names1[i], names2[i], name, length), file=meta_file_handle)
    return meta_file_path

def find_minimum_energies(energies : pd.DataFrame, meta_file : pd.DataFrame, threshold) -> np.ndarray:

    #print(energies)
    #print(meta_file)
    data = pd.merge(energies, meta_file, on='seq')

    min_e = data.loc[data.groupby('seq')['dope'].idxmin()]
    min_e['ndope'] = min_e['dope']/min_e['length']
    min_e['prediction'] = np.where(min_e['ndope'] < threshold, 1, 0)

    return min_e.values

def save_results_to_file(results : np.ndarray, initial_data : pd.DataFrame, output_folder : Path) -> Path:
    #names_list1 = initial_data['protein1']
    #names_list2 = initial_data['protein2']
    result_file_path = output_folder.joinpath('results.csv')
    with open(result_file_path, 'w') as results_file:
        #print(results)
        print('pair,protein1,protein2,score,classification', file=results_file)
        for i in range(len(results)):
            print("%d,%s,%s,%3.2f,%d" % (i, results[i,-5], results[i,-4],  results[i,-2],results[i,-1]), file=results_file)
    return result_file_path
