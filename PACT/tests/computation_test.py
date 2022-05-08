import pandas as pd
import os
from pathlib import Path

from PACT.src.computation import runModeller, compute_cross_model_interactions_concurently, cross_model

def test_runModeller(tmp_path):
	alignment_file_path = Path('/PACT/PACT/res/alignment.pir')
	output_dir = tmp_path
	result = runModeller(alignment_file_path, output_dir)
	assert(os.path.exists(output_dir))

def test_cross_model(tmp_path):
	input_file = Path('/PACT/PACT/res/example.csv')
	output_dir = tmp_path
	data = pd.read_csv(input_file)

	seq_list1 = data['seq1']
	seq_list2 = data['seq2']
	
	for i in range(len(seq_list1)):
		seq1 = str(seq_list1[i])
		seq2 = str(seq_list2[i])
		output_subdir = output_dir.joinpath(str(i))
		cross_model(seq1,seq2, output_subdir)
		assert(os.path.exists(output_subdir))

def test_compute_cross_model_interactions_concurently(tmp_path):
    input_file = Path('/PACT/PACT/res/example.csv')
    output_dir = tmp_path
    inputData = pd.read_csv(input_file)
    compute_cross_model_interactions_concurently(inputData, output_dir)
    assert(os.path.exists(output_dir))
