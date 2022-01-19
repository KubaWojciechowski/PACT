import pandas as pd
import numpy as np
import os

def compute_scores(data: pd.DataFrame, output_path: str,threshold):

    names_list1 = data['interactor']
    names_list2 = data['interactee']

    # Scoring
    os.chdir(output_path)

    # how we now that ../scripts/data.sh is there? ; If I were to pip install pact then I should be able to use it anywhere
    os.link('../scripts/data.sh', 'data.sh')

    # Can we do it without using bash scripts???
    run_script("bash data.sh > energy.csv")

    data = pd.read_csv("energy.csv")
    meta = pd.read_csv("meta.csv")
    data = pd.merge(data, meta, on='seq')

    min_e = data.loc[data.groupby('seq')['dope'].idxmin()]
    min_e['ndope'] = min_e['dope']/min_e['length']
    min_e['prediction'] = np.where(min_e['ndope'] < threshold, 1, 0)

    results = min_e.values

    results_file = open('results.csv', 'w')

    # should be behind verbose flag
    # because we don't need it in web application
    print('pair,interactor,interactee,score,classification', file=results_file)
    for i in range(len(results)):
        #print("%d,%s,%s,%s,%s,%3.2f,%d" % (i, names_list1[i], seq_list1[i], names_list2[i], seq_list2[i],  results[i,-2],results[i,-1]))
        print("%d,%s,%s,%3.2f,%d" % (
            i, names_list1[i], names_list2[i],  results[i, -2], results[i, -1]), file=results_file)

    results_file.close()

