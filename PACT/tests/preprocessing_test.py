from pact_core.preprocessing import SequencePreprocessor
import os

# should be in some constants file
fasta_file = '/PACT/PACT/res/templates.fasta'

def test_align_sequences():
	seq_1 = "KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY"
	seq_2 = "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV"
	t_seq = "KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY"
	expected_seq1 = "-KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY-"
	expected_seq2 = "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV"
	expected_t_seq = "-KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY-"
	preprocessor = SequencePreprocessor()
	seq_1, seq_2, t_seq = preprocessor.align_sequences(seq_1, seq_2, t_seq)
	assert(seq_1 == expected_seq1)
	assert(seq_2 == expected_seq2)
	assert(t_seq == expected_t_seq)

def test_get_template_sequence():
	structure = 'iapp'
	preprocessor = SequencePreprocessor()
	sequence = preprocessor.get_sequence_of_structure(structure)
	assert(sequence == "KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY")

def test_create_alignment_file(tmp_path):
	preprocessor = SequencePreprocessor()
	seq_1 = "KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY"
	seq_2 = "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV"
	output_dir = tmp_path
	preprocessor.create_alignment_file(seq_1, seq_2, 'iapp', output_dir)
	assert(os.path.exists(output_dir))