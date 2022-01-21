from PACT.src.input_validation import is_sequence_well_formed
from PACT.src.input_validation import is_input_file_well_formed

def test_sequence_validation():
    sequence = "ACACACACACACACAC"
    assert is_sequence_well_formed(sequence) == True
