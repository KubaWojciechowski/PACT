import concurrent.futures

import pandas as pd
from modeller import *
from modeller.automodel import *

from preprocessing import create_alignment_file

from constants import TEMPLATES_FASTA

def runModeller(pathToAlignmentFile : str, templates):
    class MyModel(automodel):
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

    env = environ()
    # directories for input atom files
    env.io.atom_files_directory = ['.','../atom_files']

    # Be sure to use 'MyModel' rather than 'automodel' here!
    a = MyModel(env,
                alnfile = pathToAlignmentFile,
                knowns = templates,
                sequence = 'sequence',
                assess_methods = (assess.DOPE, assess.GA341))

    a.starting_model = 1
    a.ending_model = 10

    a.make()

    return a.outputs

def cross_model(seq1, seq2):
    structure = ('iapp')
    alignmentFile = create_alignment_file(seq1, seq2,structure,TEMPLATES_FASTA) # creates alignment file
    # This also needs to know templates, script we have as python function
    outputs = runModeller(alignmentFile, structure)
    return outputs



def compute_cross_model_interactions_concurently(data: pd.DataFrame):
    seq_list1 = data['seq1']
    seq_list2 = data['seq2']

    # do we really need it here?
    # Can we do it in memory?
    meta_file = open(output_path+'/meta.csv', 'w')

    print("seq,length", file=meta_file)

    # Here Thread executor will be much faster
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(len(seq_list1)):

            name = "pair_" + str(i)
            length = (len(seq_list1[i])+len(seq_list2[i]))/2
            print("%s,%f" % (name, length), file=meta_file)

            seq1 = str(seq_list1[i])
            seq2 = str(seq_list2[i])

            future = executor.submit(cross_model, seq1, seq2)
    meta_file.close()
    return future.results()