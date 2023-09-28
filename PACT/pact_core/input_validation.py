import re
import pandas as pd
from pathlib import Path


def is_sequence_well_formed(seq: str) -> bool:
    if re.search("[A-Y]{14,45}", seq) and re.search("^((?!B|J|O|U|X).)*$", seq) and len(seq) <=45:
        return True
    return False


def is_input_file_well_formed(input_file: Path) -> bool:
    if not input_file.exists():
        raise RuntimeError(f"Input file {input_file} does not exist")

    data = pd.read_csv(input_file)

    if not (data.columns == ['protein1', 'seq1', 'protein2', 'seq2'
                             ]).all():
        return False

    seq_list1 = data['seq1']
    seq_list2 = data['seq2']

    for seq1, seq2 in zip(seq_list1, seq_list2):
        if (not (is_sequence_well_formed(seq1)
                 and is_sequence_well_formed(seq2))):
            return False
        return True
