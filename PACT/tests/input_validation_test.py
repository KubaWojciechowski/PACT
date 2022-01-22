from PACT.src.input_validation import is_sequence_well_formed
from PACT.src.input_validation import is_input_file_well_formed

def test_sequence_validation():
    sequence = "ACACACACACACACAC"
    assert is_sequence_well_formed(sequence) == True

def test_input_file_validation():
    assert is_input_file_well_formed('example.csv') == True