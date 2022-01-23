import concurrent.futures
import os

import pandas as pd
from modeller import *
from modeller.automodel import *

from PACT.src.preprocessing import create_alignment_file

def runModeller(pathToAlignmentFile : str, pathToOutputDirectory : str):
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
    env.io.atom_files_directory = ['.','/PACT/templates/']

    # Be sure to use 'MyModel' rather than 'automodel' here!
    a = MyModel(env,
                alnfile = pathToAlignmentFile,
                knowns = 'template',
                sequence = 'sequence',
                assess_methods = (assess.DOPE, assess.GA341))

    a.starting_model = 1
    a.ending_model = 10
    cwd = os.getcwd()
    if os.path.exists(pathToOutputDirectory):
        os.chdir(pathToOutputDirectory)
        a.make()
    else:
        os.mkdir(pathToOutputDirectory)
        os.chdir(pathToOutputDirectory)
        a.make()
    os.chdir(cwd)

    return a.outputs

def cross_model(seq1, seq2, name, pathToOutputDirectory:str):
    structure = ('iapp')
    TEMPLATES_FASTA = '/PACT/PACT/tests/templates.fasta'
    for template in ['iapp']:
        model_path = pathToOutputDirectory + name + template
        alignmentFilePath = create_alignment_file(seq1, seq2, structure, TEMPLATES_FASTA, model_path) # creates alignment file
        fullPath = '/PACT/' + str(alignmentFilePath)
        outputs = runModeller(fullPath, model_path)
    return outputs



def compute_cross_model_interactions_concurently(inputData: pd.DataFrame, outputDirectory:str):
    seq_list1 = inputData['seq1']
    seq_list2 = inputData['seq2']

    # do we really need it here?
    # Can we do it in memory?
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
    meta_file = open(outputDirectory+'/meta.csv', 'w')

    print("seq,length", file=meta_file)

    # Here Thread executor will be much faster
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(len(seq_list1)):

            name = "pair_" + str(i)
            length = (len(seq_list1[i])+len(seq_list2[i]))/2
            print("%s,%f" % (name, length), file=meta_file)

            seq1 = str(seq_list1[i])
            seq2 = str(seq_list2[i])
            outputSubdirectory = outputDirectory + '/' + name + 'iapp'

            future = executor.submit(cross_model, seq1, seq2, name, outputSubdirectory)
    meta_file.close()
    return future