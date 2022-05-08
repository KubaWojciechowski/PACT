from PACT.src.input_validation import is_sequence_well_formed
from PACT.src.input_validation import is_input_file_well_formed
from pathlib import Path

def test_sequence_validation():
    sequence = "ACACACACACACACAC"
    assert is_sequence_well_formed(sequence) == True

def test_input_file_validation():
    path_to_example_file = Path('/PACT/PACT/res/example.csv')
    assert is_input_file_well_formed(path_to_example_file) == True
