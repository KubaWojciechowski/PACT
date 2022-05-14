from pact_core.input_validation import is_sequence_well_formed, is_input_file_well_formed
from pathlib import Path
from importlib import resources
import res


def test_sequence_validation():
    sequence = "ACACACACACACACAC"
    assert is_sequence_well_formed(sequence) == True

def test_input_file_validation():
	with resources.path(res,'example.csv') as example_file:
		assert is_input_file_well_formed(example_file) == True