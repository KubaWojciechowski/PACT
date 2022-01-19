import re
import pandas as pd

def is_sequence_well_formed(seq: str):
    if re.search("[A-Y]{14,45}"):
        return re.search("^((?!B|J|O|U).)*$", seq)
    return False


def is_input_file_well_formed(input_path):
    data = pd.read_csv(input_path)
    if not (data.columns == ['interactor', 'seq1', 'interactee', 'seq2']).all():
        return False

    seq_list1 = data['seq1']
    seq_list2 = data['seq2']

    for seq1, seq2 in zip(seq_list1, seq_list2):
        if(not (is_sequence_well_formed(seq1) and is_sequence_well_formed(seq2))):
            return False
    return True

