import concurrent.futures
import os
from pathlib import Path
import logging
import sys

from importlib import resources

import pandas as pd
import numpy as np
from modeller import *
from modeller.automodel import *

from pact_core.preprocessing import SequencePreprocessor
import res.templates as templates_folder

def get_templates_path() -> Path:
	with resources.path(templates_folder,'iapp.pdb') as structure_file:
		return structure_file.parent

def runModeller(alignment_file_path : Path, output_dir : Path):
	class MyModel(AutoModel):
		def special_restraints(self,aln):
			# Constrain the A and B chains to be identical (but only restrain
			# the C-alpha atoms, to reduce the number of inetratomic distances
			# that need to be calculated):
			s1 = selection(self.chains['A']).only_atom_types('CA')
			s1 = selection(self.chains['B']).only_atom_types('CA')
		def user_after_single_model(self):
			# Report on symmetry violoations greater than 1A after building
			# each model:
			self.restraints.symmetry.report(1.0)

	env = Environ()
	# directories for input atom files
	env.io.atom_files_directory = ['.',get_templates_path().__str__()]

	# Be sure to use 'MyModel' rather than 'automodel' here!
	a = MyModel(env,
                alnfile = str(alignment_file_path),
                knowns = 'template',
                sequence = 'sequence',
                assess_methods = (assess.DOPE, assess.GA341))

	a.starting_model = 1
	a.ending_model = 10
	cwd = os.getcwd()
	if output_dir.exists():
		os.chdir(output_dir)
		a.make()
	else:
		os.mkdir(output_dir)
		os.chdir(output_dir)
		a.make()
	os.chdir(cwd)

	return a.outputs

def parse_modeller_result(modeller_result) -> np.array:
	scores = []
	for model in modeller_result:
		scores.append([str(int(model['name'][-6:-4]))] + [str(model['molpdf']), str(model['DOPE score']), str(model['GA341 score'][0])])
	return np.array(scores)

def save_energy_file(energies : np.array, output_dir: Path, structure : str) -> Path:
    # Should use Path for all file manipulations
	base_path = output_dir
	output_file = output_dir.parent.joinpath('energy.csv')
	with open(output_file,'a') as out_file:
		for i in energies:
			print("%s,%s,%s,%s,%s,%s" % (base_path.name, structure, i[0], i[1], i[2], i[3]), file=out_file)
	return output_file

def parse_and_save_energies(modeller_result, output_dir : Path, structure : str) -> Path:
	energies = parse_modeller_result(modeller_result)
	print(energies)
	return save_energy_file(energies, output_dir, structure)

def cross_model(seq1 : str, seq2 : str, output_dir : Path):
	if not output_dir.exists():
		logging.info(msg=f"Cross model {output_dir} does not exists, creating")
		os.mkdir(output_dir)
	
	processor = SequencePreprocessor()
	base_path = output_dir
	for structure in ['iapp']: # should be parametrized
		model_path = output_dir.joinpath(structure)
		alignment_file_path = processor.create_alignment_file(seq1, seq2, structure, model_path)
		print(alignment_file_path.absolute())
		#sys.exit()
		results = runModeller(alignment_file_path.absolute(), model_path)
		parse_and_save_energies(results, base_path, structure)
	return results

def compute_cross_model_interactions_concurently(input_data : pd.DataFrame, output_dir : Path):
	if not output_dir.exists():
		logging.info(f"Output directory {output_dir} does not exists, creating")
		os.mkdir(output_dir)

	seq_list1 = input_data['seq1']
	seq_list2 = input_data['seq2']

	with open(output_dir.joinpath('energy.csv'), 'w') as energy_file:
		print("seq,class,model,molpdf,dope,ga341", file=energy_file)

	with open(output_dir.joinpath('/meta.csv'), 'w') as meta_file:

		print("seq,length", file=meta_file)

		with concurrent.futures.ProcessPoolExecutor() as executor:
			for i in range(len(seq_list1)):
				name = "pair_" + str(i)
				length = (len(seq_list1[i])+len(seq_list2[i]))/2
				print("%s,%f" % (name, length), file=meta_file)

				seq1 = str(seq_list1[i])
				seq2 = str(seq_list2[i])
				output_subdir = output_dir.joinpath(name)

				future = executor.submit(cross_model, seq1, seq2, output_subdir)
	return future
