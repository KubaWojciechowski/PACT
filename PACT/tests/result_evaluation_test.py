import os
from pathlib import Path
import pandas as pd
import numpy as np
from pact_core.result_evaluation import create_meta_file, find_minimum_energies, save_results_to_file
from pact_core.computation import compute_cross_model_interactions_concurently
from importlib import resources
import res
def test_create_meta_file(tmp_path):
	with resources.path(res,'example.csv') as input_file:
		data = pd.read_csv(input_file)
	output_dir = tmp_path
	seq_list1 = data['seq1']
	seq_list2 = data['seq2']
	meta_file_path = create_meta_file(seq_list1, seq_list2, output_dir)
	assert(os.path.exists(meta_file_path))

def test_find_minimum_energies(tmp_path):
	with resources.path(res,'example.csv') as input_file:
		data = pd.read_csv(input_file)
	output_dir = tmp_path
	
	seq_list1 = data['seq1']
	seq_list2 = data['seq2']
	
	meta_file_path = create_meta_file(seq_list1, seq_list2, output_dir)
	compute_cross_model_interactions_concurently(data, output_dir)
	meta_file = pd.read_csv(meta_file_path)
	energy_file_path = output_dir.joinpath('energy.csv')
	energies = pd.read_csv(energy_file_path)
	min_energies = find_minimum_energies(energies, meta_file, 236)
	assert(len(min_energies) == 2)
	results_file = save_results_to_file(min_energies, data, output_dir)
	assert(os.path.exists(str(results_file)))